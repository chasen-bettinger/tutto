from securesystemslib.dsse import Envelope as SSLibEnvelope
from securesystemslib.signer import Signer

from signable import Signable
from metadata import Metadata
import attr
import json


class Envelope(SSLibEnvelope, Metadata):
    @classmethod
    def from_signable(cls, signable: Signable):
        json_bytes = json.dumps(attr.asdict(signable), sort_keys=True).encode("utf-8")

        return cls(
            payload=json_bytes,
            payload_type="application/vnd.in-toto+json",
            signatures=[],
        )

    def create_signature(self, signer: Signer):
        return super().sign(signer)
