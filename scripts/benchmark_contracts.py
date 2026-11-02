"""Small shared contracts for benchmark configuration, not workflow decisions."""
from pathlib import Path


def forbidden_file_paths(value: object) -> list[str]:
    """Accept an array of nonempty relative paths; reject invalid configuration."""
    if not isinstance(value, list):
        raise ValueError("forbidden_files must be an array")
    paths = []
    for index, relative in enumerate(value):
        if not isinstance(relative, str) or not relative.strip() or "\0" in relative:
            raise ValueError(f"forbidden_files[{index}] must be a nonempty relative path")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError(f"forbidden_files[{index}] unsafe relative path: {relative!r}")
        paths.append(relative)
    return paths
