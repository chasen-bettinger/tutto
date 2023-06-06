import attr
from supply_chain_item import SupplyChainItem


@attr.s(repr=False, init=False)
class Step(SupplyChainItem):
    _type = attr.ib()
    pubkeys = attr.ib()
    expected_command = attr.ib()
    threshold = attr.ib()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._type = "step"
        self.pubkeys = kwargs.get("pubkeys", {})
        self.expected_command = kwargs.get("expected_command", [])
        self.threshold = kwargs.get("threshold", 0)

    @staticmethod
    def read(data):
        return Step(**data)
