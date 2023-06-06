import securesystemslib.formats
import attr
import json


class Signable:
    """Objects with base class Signable are to be included in a Metablock class
    to be signed (hence the name). They provide a `signable_bytes` property
    used to create deterministic signatures."""

    def __repr__(self):
        """Returns an indented JSON string of the metadata object."""
        return json.dumps(
            attr.asdict(self), indent=1, separators=(",", ": "), sort_keys=True
        )

    @property
    def signable_bytes(self):
        """The UTF-8 encoded canonical JSON byte representation of the dictionary
        representation of the instance."""
        canonically_encoded = securesystemslib.formats.encode_canonical(
            attr.asdict(self)
        )
        if canonically_encoded is None:
            raise ValueError("Could not canonicalize the object.")

        return canonically_encoded.encode("UTF-8")
