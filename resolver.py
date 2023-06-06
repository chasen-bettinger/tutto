import logging
from itertools import combinations
from pathspec import GitIgnoreSpec
from os.path import exists, isfile, normpath
from securesystemslib.hash import digest_filename


# pyright: reportGeneralTypeIssues=false
logging.basicConfig(level=logging.NOTSET)
# logging.root.setLevel(logging.INFO)
logger = logging.getLogger(None)


class AResolver:
    def __init__(
        self,
        exclude_patterns=[],
        base_path=None,
        follow_symlink_dirs=False,
        normalize_line_endings=False,
        lstrip_paths=None,
    ):
        if exclude_patterns is None:
            exclude_patterns = []
        if not lstrip_paths:
            lstrip_paths = []
        if base_path is None:
            if not isinstance(base_path, str):
                raise ValueError("'base_path' must be a string")
        for name, val in [
            ("exclude_patterns", exclude_patterns),
            ("lstrip_paths", lstrip_paths),
        ]:
            if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
                raise ValueError(f"'{name}' must be a list")

        for a, b in combinations(lstrip_paths, 2):
            if a.startswith(b) or b.startswith(a):
                raise ValueError(f"lstrip_paths {a} and {b} conflict")

        self._exclude_filter = GitIgnoreSpec.from_lines(
            "gitwildmatch", exclude_patterns
        )
        self._base_path = base_path
        self._follow_symlink_dirs = follow_symlink_dirs
        self._normalize_line_endings = normalize_line_endings
        self._lstrip_paths = lstrip_paths

    def _exclude(self, path):
        return self._exclude_filter.match_file(path)

    def _mangle(self, path, existing_paths, scheme_prefix):
        # Normalize slashes for cross-platform metadata consistency
        path = path.replace("\\", "/")

        # Left-strip names using configured path prefixes
        for lstrip_path in self._lstrip_paths:
            if path.startswith(lstrip_path):
                path = path[len(lstrip_path) :]
                break

        # Fail if left-stripping above results in duplicates
        if self._lstrip_paths and path in existing_paths:
            raise Exception(
                "Prefix selection has resulted in non unique dictionary key "
                f"'{path}'"
            )

        # Prepend passed scheme prefix
        path = scheme_prefix + path

        return path

    def _hash(self, path):
        digest = digest_filename(
            path,
            algorithm="sha256",
            normalize_line_endings=self._normalize_line_endings,
        )
        return {"sha256": digest.hexdigest()}

    def hash_artifacts(self, uris):
        hashes = {}
        for path in uris:
            path = normpath(path)
            logger.info(path)
            if self._exclude(path):
                logger.info("Skipping excluded path: %s", path)
                continue
            if not exists(path):
                logger.info("Skipping non-existent path: %s", path)
                continue

            if isfile(path):
                logger.info("Hashing file: %s", path)

                # INFO:root:name: file:demo-project/foo.py
                name = self._mangle(path, hashes, "file:")
                logger.info("name: %s", name)

                hashes[name] = self._hash(path)

        return hashes
