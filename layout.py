import attr
from step import Step


class Layout:
    _type = attr.ib()
    steps = attr.ib()
    inspect = attr.ib()
    keys = attr.ib()
    expires = attr.ib()
    readme = attr.ib()

    def __init__(self, **kwargs):
        self._type = "layout"
        self.steps = kwargs.get("steps", [])
        self.inspect = kwargs.get("inspect", [])
        self.keys = kwargs.get("keys", {})
        self.readme = kwargs.get("readme", "")

    @staticmethod
    def read(data):
        steps = []
        for step in data.get("steps", []):
            steps.append(Step.read(step))
