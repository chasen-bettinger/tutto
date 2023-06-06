import attr
from signable import Signable


@attr.s(repr=False, init=False)
class Link(Signable):
    name = attr.ib()
    materials = attr.ib()
    products = attr.ib()
    command = attr.ib()
    byproducts = attr.ib()
    environment = attr.ib()

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.name = kwargs.get("name")
        self.materials = kwargs.get("materials")
        self.products = kwargs.get("products")
        self.command = kwargs.get("command")
        self.byproducts = kwargs.get("byproducts")
        self.environment = kwargs.get("environment")
