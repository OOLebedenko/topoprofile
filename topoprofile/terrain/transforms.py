from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import rasterio
from click.testing import CliRunner
from rio_rgbify.scripts.cli import rgbify

from topoprofile.processing.transforms import Transform
from topoprofile.terrain.models import DEM, RasterTile

type DEMTransform = Transform[DEM]
type TerrainTileTransform = Transform[RasterTile]


class ConvertToInt16:
    """Round DEM elevations and convert them to int16."""

    def __call__(
            self,
            dem: DEM,
    ) -> DEM:
        values = np.rint(
            dem.values,
        ).astype(np.int16)

        return DEM(
            values=values,
            transform=dem.transform,
            crs=dem.crs,
            nodata=dem.nodata,
        )


class TerrariumConversionError(RuntimeError):
    """Raised when Terrarium conversion fails."""


class TerrariumTransform:
    """Convert DEM elevations to Terrarium encoding."""

    def __call__(
            self,
            dem: DEM,
    ) -> DEM:
        with TemporaryDirectory(
                prefix="topoprofile-terrarium-",
        ) as temp_dir:
            temp_root = Path(temp_dir)
            input_path = temp_root / "dem.tif"
            output_path = temp_root / "dem_terrarium.tif"

            self._write_dem(
                dem=dem,
                output_path=input_path,
            )
            self._convert(
                input_path=input_path,
                output_path=output_path,
            )

            return self._read_dem(output_path)

    def _write_dem(
            self,
            dem: DEM,
            output_path: Path,
    ) -> None:
        with rasterio.open(
                output_path,
                "w",
                driver="GTiff",
                height=dem.height,
                width=dem.width,
                count=1,
                dtype=dem.values.dtype,
                crs=dem.crs,
                transform=dem.transform,
                nodata=dem.nodata,
        ) as dataset:
            dataset.write(
                dem.values,
                1,
            )

    def _convert(
            self,
            input_path: Path,
            output_path: Path,
    ) -> None:
        runner = CliRunner()

        result = runner.invoke(
            rgbify,
            [
                "--base-val",
                "-32768",
                "--interval",
                "0.00390625",
                "--co",
                "TILED=YES",
                "--co",
                "BLOCKXSIZE=256",
                "--co",
                "BLOCKYSIZE=256",
                str(input_path),
                str(output_path),
            ],
        )

        if result.exit_code != 0:
            raise TerrariumConversionError(
                f"rio-rgbify failed with exit code {result.exit_code}"
            ) from result.exception

        if not output_path.is_file():
            raise TerrariumConversionError(
                "rio-rgbify completed successfully, but the output file "
                f"was not created: {output_path}"
            )

    def _read_dem(
            self,
            input_path: Path,
    ) -> DEM:
        with rasterio.open(input_path) as dataset:
            values = dataset.read()

            return DEM(
                values=values,
                transform=dataset.transform,
                crs=dataset.crs,
                nodata=dataset.nodata,
            )
