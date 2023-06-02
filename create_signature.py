def create_signature(key_dict, data):
    signature = {}
    keytype = key_dict["keytype"]
    scheme = key_dict["scheme"]
    public = key_dict["keyval"]["public"]
    private = key_dict["keyval"]["private"]
    keyid = key_dict["keyid"]
    sig = None

    private = private.replace("\r\n", "\n")
    # TODO: implement create rsa signature
    # sig, scheme = rsa_key.

    return signature
