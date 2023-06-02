import attr


class SupplyChainItem:
    name = attr.ib()
    expected_materials = attr.ib()
    expected_products = attr.ib()

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.expected_materials = kwargs.get("expected_materials", [])
        self.expected_products = kwargs.get("expected_products", [])
