import attr
import json


@attr.s(repr=False, init=False)
class SupplyChainItem:
    name = attr.ib()
    expected_materials = attr.ib()
    expected_products = attr.ib()

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.expected_materials = kwargs.get("expected_materials", [])
        self.expected_products = kwargs.get("expected_products", [])

    def __repr__(self):
        """Returns an indented JSON string of the metadata object."""
        return json.dumps(
            attr.asdict(self), indent=1, separators=(",", ": "), sort_keys=True
        )
