import hashlib
from contextlib import contextmanager
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac, serialization


@contextmanager
def _get_file(filepath):
    try:
        file_object = open(filepath, "rb")
        yield file_object
    except OSError:
        raise "Can't open %s" % filepath

    finally:
        if file_object is not None:
            file_object.close()


def _get_public_private_from_pem(pem_key, passphrase=None):
    if passphrase is not None:
        passphrase = passphrase.encode("utf-8")

    # 1. Acquire RSAPrivateKey + RSAPublicKey Objects
    private_key = load_pem_private_key(
        pem_key.encode("utf-8"), passphrase, backend=default_backend()
    )
    public_key = private_key.public_key()

    # 2. Convert RSA Objects to byte representations
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).strip()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).strip()

    # 3. Convert byte representations to strings
    return public_pem.decode(), private_pem.decode()


def _extract_pem(pem, private_pem=False):
    if private_pem:
        pem_header = "-----BEGIN RSA PRIVATE KEY-----"
        pem_footer = "-----END RSA PRIVATE KEY-----"

    else:
        pem_header = "-----BEGIN PUBLIC KEY-----"
        pem_footer = "-----END PUBLIC KEY-----"

    header_start = 0
    footer_start = 0

    header_start = pem.index(pem_header)
    footer_start = pem.index(pem_footer, header_start + len(pem_header))
    # Extract only the public portion of 'pem'.  Leading or trailing whitespace
    # is excluded.
    pem = pem[header_start : footer_start + len(pem_footer)]

    return pem


def _format_keyval_to_metadata(keytype, scheme, key_value, private=False):
    if private is True:
        # If the caller requests (via the 'private' argument) to include a private
        # key in the returned dictionary, ensure the private key is actually
        # present in 'key_val' (a private key is optional for 'KEYVAL_SCHEMA'
        # dicts).
        if "private" not in key_value:
            raise Exception(
                "The required private key is missing from: " + repr(key_value)
            )

        return {"keytype": keytype, "scheme": scheme, "keyval": key_value}

    public_key_value = {"public": key_value["public"]}

    return {
        "keytype": keytype,
        "scheme": scheme,
        "keyid_hash_algorithms": ["sha256", "sha512"],
        "keyval": public_key_value,
    }


def _canonical_string_encoder(string):
    """
    <Purpose>
      Encode 'string' to canonical string format.

    <Arguments>
      string:
        The string to encode.

    <Exceptions>
      None.

    <Side Effects>
      None.

    <Returns>
      A string with the canonical-encoded 'string' embedded.
    """

    string = '"%s"' % string.replace("\\", "\\\\").replace('"', '\\"')

    return string


def __encode_canonical(
    object, output_function
):  # pylint: disable=missing-function-docstring,redefined-builtin
    # Helper for encode_canonical.  Older versions of json.encoder don't
    # even let us replace the separators.

    if isinstance(object, str):
        output_function(_canonical_string_encoder(object))
    elif object is True:
        output_function("true")
    elif object is False:
        output_function("false")
    elif object is None:
        output_function("null")
    elif isinstance(object, int):
        output_function(str(object))
    elif isinstance(object, (tuple, list)):
        output_function("[")
        if len(object):
            for item in object[:-1]:
                _encode_canonical(item, output_function)
                output_function(",")
            _encode_canonical(object[-1], output_function)
        output_function("]")
    elif isinstance(object, dict):
        output_function("{")
        if len(object):
            items = sorted(object.items())
            for key, value in items[:-1]:
                output_function(_canonical_string_encoder(key))
                output_function(":")
                _encode_canonical(value, output_function)
                output_function(",")
            key, value = items[-1]
            output_function(_canonical_string_encoder(key))
            output_function(":")
            _encode_canonical(value, output_function)
        output_function("}")
    else:
        raise Exception("I cannot encode " + repr(object))


def _encode_canonical(object, output_function=None):
    result = None
    # If 'output_function' is unset, treat it as
    # appending to a list.
    if output_function is None:
        result = []
        output_function = result.append

    try:
        __encode_canonical(object, output_function)

    except TypeError as e:
        message = "Could not encode " + repr(object) + ": " + str(e)
        raise Exception(message)

    # Return the encoded 'object' as a string.
    # Note: Implies 'output_function' is None,
    # otherwise results are sent to 'output_function'.
    if result is not None:
        return "".join(result)


def _get_keyid(keytype, scheme, key_value):
    """Return the keyid of 'key_value'."""

    # 'keyid' will be generated from an object conformant to KEY_SCHEMA,
    # which is the format Metadata files (e.g., root.json) store keys.
    # 'format_keyval_to_metadata()' returns the object needed by _get_keyid().
    key_meta = _format_keyval_to_metadata(keytype, scheme, key_value, private=False)

    # Convert the key to JSON Canonical format, suitable for adding
    # to digest objects.
    key_update_data = _encode_canonical(key_meta)
    if key_update_data is None:
        return

    # Create a digest object and call update(), using the JSON
    # canonical format of 'rskey_meta' as the update data.
    digest_object = hashlib.new("sha256")
    digest_object.update(key_update_data.encode("utf-8"))

    # 'keyid' becomes the hexadecimal representation of the hash.
    keyid = digest_object.hexdigest()

    return keyid


def import_private_key(filepath):
    print("importing private key...")

    # 1. Read the private key file
    file_object = None
    with _get_file(filepath) as file_object:
        pem_key = file_object.read().decode("utf-8")

    # 2. With the private key file as a string,
    # parse the string into a RSAPrivateKey object
    # and from that object, retrieve the private
    # public key pair.
    public, private = _get_public_private_from_pem(pem_key)

    # TODO: this was in the original code, but I do not
    # understand why it is necessary. Reevaluate later
    # as a learning opportunity.
    # print(":::private before:::")
    # print(private)
    # public = _extract_pem(public, private_pem=False)
    # private = _extract_pem(private, private_pem=True)
    # print(":::private after:::")
    # print(private)

    # 3. Generate keyvalue dictionary
    key_value = {"public": public.replace("\r\n", "\n"), "private": ""}

    key_type = "rsa"
    key_scheme = "rsassa-pss-sha256"

    # The digest of metadata from the public key
    key_id = _get_keyid(key_type, key_scheme, key_value)

    #   Build the 'rsakey_dict' dictionary.  Update 'key_value' with the RSA
    #   private key prior to adding 'key_value' to 'rsakey_dict'.
    key_value["private"] = private

    # 4. Put together the return value
    rsakey_dict = {}

    rsakey_dict["keytype"] = key_type
    rsakey_dict["scheme"] = key_scheme
    rsakey_dict["keyid"] = key_id
    rsakey_dict["keyval"] = key_value

    return rsakey_dict
