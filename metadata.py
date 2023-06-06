import json


class Metadata:
    def to_dict(self):
        """Returns the JSON-serializable dictionary representation of self."""
        raise NotImplementedError  # pragma: no cover

    def dump(self, path):
        """Writes the JSON string representation of the instance to disk.

        Arguments:
          path: The path to write the file to.

        Raises:
          IOError: File cannot be written.

        """
        json_bytes = json.dumps(
            self.to_dict(),
            sort_keys=True,
        ).encode("utf-8")

        with open(path, "wb") as fp:
            fp.write(json_bytes)
