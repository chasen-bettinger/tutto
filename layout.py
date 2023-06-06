import attr
from step import Step
from inspection import Inspection
from signable import Signable


@attr.s(repr=False, init=False)
class Layout(Signable):
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
        self.expires = kwargs.get("expires", None)

    @staticmethod
    def read(data):
        steps = []
        for step in data.get("steps", []):
            steps.append(Step.read(step))

        inspections = []
        for inspection in data.get("inspect", []):
            inspections.append(Inspection.read(inspection))

        data["steps"] = steps
        data["inspect"] = inspections
        return Layout(**data)
