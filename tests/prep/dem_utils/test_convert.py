from pathlib import Path
from types import SimpleNamespace

import pytest

from topoprofile.prep.dem_utils import convert


@pytest.fixture
def fake_runner_factory():
    """Return a factory that creates a fake CliRunner and a calls dict."""

    def factory(
        *,
        exit_code: int,
        output: str = "",
        exception: Exception | None = None,
        create_output: bool = False,
    ):
        calls = {}

        class FakeRunner:
            def invoke(self, command, args):
                calls["command"] = command
                calls["args"] = args

                if create_output:
                    Path(args[-1]).touch()

                return SimpleNamespace(
                    exit_code=exit_code,
                    output=output,
                    exception=exception,
                )

        return FakeRunner, calls

    return factory


def test_convert_returns_existing_output(tmp_path: Path) -> None:
    """Return existing output without conversion when force_convert=False."""
    input_path = tmp_path / "dem.tif"
    output_path = tmp_path / "dem_terrarium.tif"

    input_path.touch()
    output_path.touch()

    result = convert.convert_dem_to_terrarium(
        input_path=input_path,
        output_path=output_path,
    )

    assert result == output_path


def test_convert_raises_if_input_missing(tmp_path: Path) -> None:
    """Raise FileNotFoundError when input DEM does not exist."""
    with pytest.raises(FileNotFoundError):
        convert.convert_dem_to_terrarium(
            input_path=tmp_path / "missing.tif",
            output_path=tmp_path / "dem_terrarium.tif",
        )


def test_convert_calls_rgbify(
    monkeypatch,
    tmp_path: Path,
    fake_runner_factory,
) -> None:
    """Verify that rio-rgbify is invoked with correct arguments."""
    input_path = tmp_path / "dem.tif"
    output_path = tmp_path / "dem_terrarium.tif"

    input_path.touch()

    fake_runner_cls, calls = fake_runner_factory(
        exit_code=0,
        create_output=True,
    )

    monkeypatch.setattr(
        convert,
        "CliRunner",
        fake_runner_cls,
    )

    result = convert.convert_dem_to_terrarium(
        input_path=input_path,
        output_path=output_path,
    )

    assert result == output_path
    assert calls["command"] is convert.rgbify


def test_convert_raises_conversion_error(
    monkeypatch,
    tmp_path: Path,
    fake_runner_factory,
) -> None:
    """Raise ConversionError when rio-rgbify fails."""
    input_path = tmp_path / "dem.tif"
    output_path = tmp_path / "dem_terrarium.tif"

    input_path.touch()

    fake_runner_cls, _ = fake_runner_factory(
        exit_code=1,
        output="rgbify failed",
        exception=RuntimeError("rgbify failed"),
    )

    monkeypatch.setattr(
        convert,
        "CliRunner",
        fake_runner_cls,
    )

    with pytest.raises(
        convert.ConversionError,
        match="rio-rgbify failed with exit code 1",
    ):
        convert.convert_dem_to_terrarium(
            input_path=input_path,
            output_path=output_path,
        )


def test_convert_raises_if_output_not_created(
    monkeypatch,
    tmp_path: Path,
    fake_runner_factory,
) -> None:
    """Raise ConversionError when rgbify succeeds but creates no file."""
    input_path = tmp_path / "dem.tif"
    output_path = tmp_path / "dem_terrarium.tif"

    input_path.touch()

    fake_runner_cls, _ = fake_runner_factory(
        exit_code=0,
        create_output=False,
    )

    monkeypatch.setattr(
        convert,
        "CliRunner",
        fake_runner_cls,
    )

    with pytest.raises(
        convert.ConversionError,
        match="output file was not created",
    ):
        convert.convert_dem_to_terrarium(
            input_path=input_path,
            output_path=output_path,
        )
