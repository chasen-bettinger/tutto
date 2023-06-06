from import_private_key import import_private_key
from layout import Layout
from metablock import Metablock
from run import run
import shutil

# 0. cleanup
shutil.rmtree("./demo-project", ignore_errors=True)

# 1. Creating a dictionary in a format that allows us
# to create a signer that will eventually be signing
# the layout.
# We need a private key in order to generate a signer.
# Project owner is the label used to describe the
# individual that is responsible for defining
# the layout.
project_owner = import_private_key("./chasen")

# 2. Add entities that are enable to do things within
# the supply chain (functionaries)
brendan_functionary = import_private_key("./brendan")

artifact_created_from_clone = "demo-project/foo.py"

# 3. Create a layout. This defines what is going to happen
# within the supply chain.
layout = Layout.read(
    {
        "keys": {brendan_functionary["keyid"]: brendan_functionary},
        "steps": [
            {
                "name": "clone",
                "expected_materials": [],
                "expected_products": [
                    ["CREATE", artifact_created_from_clone],
                    ["DISALLOW", "*"],
                ],
                "pubkeys": [brendan_functionary["keyid"]],
                "expected_command": [
                    "git",
                    "clone",
                    "https://github.com/in-toto/demo-project.git",
                ],
                "threshold": 1,
            }
        ],
    }
)

# 4. Put the layout in a format that we can then sign.
metadata = Metablock(signed=layout)

# 5. Sign the layout with the project owner's private key.
# TODO: what happens if there is no signature?
metadata.sign(project_owner)

# output looks like this:
# [{'keyid': 'e39dfe07f2eb1658e15bf27f2813ec36d2bfb5b9efb3296f10fc6cd7f62fe8f9',
# 'sig': '08e7cea28dcd43c46bdeb1e0d1bd07dfe6bc505ecd0d1e123d6c430c7f369ca1b6ee9c050abfe2e3a8c15617607033d5a33b2dac7a668c42bfb4bcdcfacab49b50799327b067ee99d542795f0073a998df22c42d1e959f7152acb8b6b20b8db8ed12c91eaf08ef67de5720fac6dcfc6d2b9d0213f44985bcd6e63f9528ecf8a2c707a438ebabf2eac1457b556caf62e1ecb4535750f0650790231e3743581b43b62897ed782d402bf013fac061ec00aa7406aefb6c8ed5e9f5b22b03047a1ff4aa22ebb3088118b03b1e065ade7f104440103ffab3284f59503c2f24b4b8fb4393911c8602ed6ecf067777050c524f1d3dbb9292fe643cf7526033ffbad1a33293998b4ad6c761488a94731f74e9da06e8c4a1dd3c0b5bccc12100e494b2ba4d3995cee3a53b3913e46d3f1a98615cb713db53e6f46f71fc37b83df3bb781ea7643479570ea73c398e70aab76753ea45cfa1bbe17cd538f5f5674d92031cb50610e1bfa11bc76485d6ae952371e6d193034fa301d5b5b0faaed2582876dea2db'}]

# 6. Save metadata to disk.
metadata.dump("root.layout")

# 7. run a command
run(
    name="clone",
    base_path=".",
    link_cmd_args=["git", "clone", "https://github.com/in-toto/demo-project.git"],
    product_list=[artifact_created_from_clone],
    signing_key=brendan_functionary,
)
