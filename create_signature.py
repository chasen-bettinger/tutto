from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)
from cryptography.hazmat.primitives import hashes as _pyca_hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import (
    rsa,
)
import binascii

# pyright: reportGeneralTypeIssues=false


def _create_rsa_signature(private_key, data):
    private_key_object: rsa.RSAPrivateKey = load_pem_private_key(
        private_key.encode("utf-8"), None
    )
    scheme = "rsassa-pss-sha256"
    signature = private_key_object.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(_pyca_hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        _pyca_hashes.SHA256(),
    )

    return signature, scheme


def create_signature(key_dict, data):
    signature = {}
    keytype = key_dict["keytype"]
    scheme = key_dict["scheme"]
    public = key_dict["keyval"]["public"]
    private = key_dict["keyval"]["private"]
    keyid = key_dict["keyid"]

    private = private.replace("\r\n", "\n")
    sig, scheme = _create_rsa_signature(private, data)

    signature["keyid"] = keyid
    signature["sig"] = binascii.hexlify(sig).decode()

    return signature
