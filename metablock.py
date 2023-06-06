import attr
import json
from metadata import Metadata
from create_signature import create_signature

# pyright: reportGeneralTypeIssues=false


class Metablock(Metadata):
    signatures = attr.ib()
    signed = attr.ib()

    def __init__(self, **kwargs):
        self.signatures = kwargs.get("signatures", [])
        self.signed = kwargs.get("signed", {})
        self.compact_json = kwargs.get("compact_json", False)

    def __repr__(self):
        """Returns the JSON string representation."""
        indent = None if self.compact_json else 1
        separators = (",", ":") if self.compact_json else (",", ": ")

        return json.dumps(
            {"signatures": self.signatures, "signed": attr.asdict(self.signed)},
            indent=indent,
            separators=separators,
            sort_keys=True,
        )

    def sign(self, key):
        signature = create_signature(key, self.signed.signable_bytes)
        self.signatures.append(signature)
        return signature

    def dump(self, path):
        """Writes the JSON string representation of the instance to disk.

        Arguments:
          path: The path to write the file to.

        Raises:
          IOError: File cannot be written.

        """
        with open(path, "wb") as fp:
            fp.write("{}".format(self).encode("utf-8"))
