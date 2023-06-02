from import_private_key import import_private_key

# 1. Creating a dictionary in the format to create a signer
# that will eventaully be signing the outputs
key_dict = import_private_key("./chasen")


# We need a private key in order to generate a signer
print(key_dict)
