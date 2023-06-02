import attr
from supply_chain_item import SupplyChainItem


class Step(SupplyChainItem):
    _type = attr.ib()
    pubkeys = attr.ib()
    expected_command = attr.ib()
    threshold = attr.ib()

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._type = "step"
        self.pubkeys = kwargs.get("pubkeys", {})
        self.expected_command = kwargs.get("expected_command", [])
        self.threshold = kwargs.get("threshold", 0)

    def read(self, data):
        return Step(**data)
