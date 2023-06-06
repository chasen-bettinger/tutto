import attr
from supply_chain_item import SupplyChainItem


class Inspection(SupplyChainItem):
    _type = attr.ib()
    run = attr.ib()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._type = "inspection"
        self.run = kwargs.get("run", [])

    @staticmethod
    def read(data):
        return Inspection(**data)
