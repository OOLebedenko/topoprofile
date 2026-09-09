import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def atomic_path(
        output_path: Path,
) -> Iterator[Path]:
    """Yield a temporary path and publish it atomically."""
    temporary_path = output_path.with_suffix(
        f".tmp{output_path.suffix}"
    )

    try:
        yield temporary_path

        os.replace(
            temporary_path,
            output_path,
        )
    finally:
        temporary_path.unlink(
            missing_ok=True,
        )
