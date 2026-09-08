from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import rasterio
from affine import Affine
from rasterio.crs import CRS

from topoprofile.terrain import transforms
from topoprofile.terrain.models import DEM
from topoprofile.terrain.transforms import (
    ConvertToInt16,
    TerrariumConversionError,
    TerrariumTransform,
)


@pytest.fixture
def dem() -> DEM:
    return DEM(
        values=np.array(
            [
                [100.4, 200.6],
                [300.2, 400.8],
            ],
            dtype=np.float32,
        ),
        transform=Affine(
            0.5,
            0.0,
            42.0,
            0.0,
            -0.5,
            44.0,
        ),
        crs=CRS.from_epsg(4326),
        nodata=None,
    )


@pytest.fixture
def fake_runner_factory():
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
                    input_path = Path(args[-2])
                    output_path = Path(args[-1])

                    with rasterio.open(input_path) as source:
                        profile = source.profile
                        profile.update(
                            count=3,
                            dtype=np.uint8,
                            nodata=None,
                        )

                        with rasterio.open(
                                output_path,
                                "w",
                                **profile,
                        ) as target:
                            target.write(
                                np.zeros(
                                    (
                                        3,
                                        source.height,
                                        source.width,
                                    ),
                                    dtype=np.uint8,
                                )
                            )

                return SimpleNamespace(
                    exit_code=exit_code,
                    output=output,
                    exception=exception,
                )

        return FakeRunner, calls

    return factory


def test_convert_to_int16(
        dem: DEM,
) -> None:
    transform = ConvertToInt16()

    result = transform(dem)

    assert result.values.dtype == np.int16

    np.testing.assert_array_equal(
        result.values,
        np.array(
            [
                [100, 201],
                [300, 401],
            ],
            dtype=np.int16,
        ),
    )

    assert result.transform == dem.transform
    assert result.crs == dem.crs
    assert result.nodata == dem.nodata


def test_terrarium_transform_calls_rgbify(
        monkeypatch,
        dem: DEM,
        fake_runner_factory,
) -> None:
    fake_runner_cls, calls = fake_runner_factory(
        exit_code=0,
        create_output=True,
    )

    monkeypatch.setattr(
        transforms,
        "CliRunner",
        fake_runner_cls,
    )

    result = TerrariumTransform()(dem)

    assert isinstance(result, DEM)
    assert result.count == 3
    assert calls["command"] is transforms.rgbify
    assert "--base-val" in calls["args"]
    assert "--interval" in calls["args"]


def test_terrarium_transform_raises_conversion_error(
        monkeypatch,
        dem: DEM,
        fake_runner_factory,
) -> None:
    fake_runner_cls, _ = fake_runner_factory(
        exit_code=1,
        output="rgbify failed",
        exception=RuntimeError("rgbify failed"),
    )

    monkeypatch.setattr(
        transforms,
        "CliRunner",
        fake_runner_cls,
    )

    with pytest.raises(
            TerrariumConversionError,
            match="rio-rgbify failed with exit code 1",
    ):
        TerrariumTransform()(dem)


def test_terrarium_transform_raises_if_output_not_created(
        monkeypatch,
        dem: DEM,
        fake_runner_factory,
) -> None:
    fake_runner_cls, _ = fake_runner_factory(
        exit_code=0,
        create_output=False,
    )

    monkeypatch.setattr(
        transforms,
        "CliRunner",
        fake_runner_cls,
    )

    with pytest.raises(
            TerrariumConversionError,
            match="output file was not created",
    ):
        TerrariumTransform()(dem)
