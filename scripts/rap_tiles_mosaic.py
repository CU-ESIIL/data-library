#!/usr/bin/env python3
"""Fetch and mosaic RAP tiles from Google Cloud Storage.

This utility downloads tiled imagery from the USDA Rangeland Analysis
Platform (RAP) tilesets and stitches them into a single image.

Example
-------
    python scripts/rap_tiles_mosaic.py \
        --vegetation pfg --year 2011 --masked \
        --bbox -105.9 40.1 -105.3 40.6 --z 10 \
        --output mosaic.png \
        --tag demo

The saved PNG includes metadata tags ``rap``, ``tiles`` and
``innovation-summit-2025`` plus any ``--tag`` values.
"""
from __future__ import annotations

import argparse
import io
import math
from pathlib import Path

import numpy as np
import requests
from PIL import Image, PngImagePlugin

try:  # optional dependency used only when --show is passed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib is optional
    plt = None


def lonlat_to_tile(lon: float, lat: float, z: int) -> tuple[int, int]:
    """Convert longitude/latitude to XYZ tile coordinates."""
    lat_rad = math.radians(lat)
    n = 2.0 ** z
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def fetch_tile_png(url: str) -> Image.Image:
    """Download a single PNG tile."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content)).convert("RGBA")


def rap_tile_mosaic(
    vegetation: str,
    year: int,
    masked: bool,
    bbox: tuple[float, float, float, float],
    z: int,
) -> np.ndarray:
    """Return a mosaic array covering the supplied bounding box."""
    west, south, east, north = bbox
    x_min, y_max = lonlat_to_tile(west, south, z)
    x_max, y_min = lonlat_to_tile(east, north, z)

    x_range = range(min(x_min, x_max), max(x_min, x_max) + 1)
    y_range = range(min(y_min, y_max), max(y_min, y_max) + 1)

    base = "masked" if masked else "unmasked"
    tileset = "usda-rap-tiles-cover-v3"

    mosaic = None
    for y in y_range:
        row_imgs = []
        for x in x_range:
            url = (
                f"https://storage.googleapis.com/{tileset}/{base}/"
                f"{vegetation}/{year}/{z}/{x}/{y}.png"
            )
            try:
                row_imgs.append(fetch_tile_png(url))
            except Exception:
                row_imgs.append(Image.new("RGBA", (256, 256), (0, 0, 0, 0)))
        row = np.hstack([np.array(im) for im in row_imgs])
        mosaic = row if mosaic is None else np.vstack([mosaic, row])
    return mosaic


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch RAP tile mosaic.")
    parser.add_argument("--vegetation", default="pfg", help="Vegetation type")
    parser.add_argument("--year", type=int, default=2011, help="Year of data")
    parser.add_argument("--masked", action="store_true", help="Use masked tiles")
    parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("W", "S", "E", "N"),
        required=True,
        help="Bounding box (west south east north)",
    )
    parser.add_argument("--z", type=int, default=10, help="Zoom level")
    parser.add_argument("-o", "--output", type=Path, help="Output PNG file")
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        metavar="TAG",
        help="Additional metadata tag (can repeat)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display result with matplotlib (requires matplotlib)",
    )
    args = parser.parse_args()

    mosaic = rap_tile_mosaic(args.vegetation, args.year, args.masked, tuple(args.bbox), args.z)
    image = Image.fromarray(mosaic)
    if args.output:
        pnginfo = PngImagePlugin.PngInfo()
        tags = ["rap", "tiles", "innovation-summit-2025", *args.tag]
        pnginfo.add_text("tags", ",".join(tags))
        image.save(args.output, pnginfo=pnginfo)
    if args.show:
        if plt is None:
            raise SystemExit("matplotlib is required for --show")
        plt.figure(figsize=(6, 6))
        plt.imshow(mosaic)
        plt.axis("off")
        title = f"RAP tiles — {args.vegetation.upper()} {args.year} ({'masked' if args.masked else 'unmasked'})"
        plt.title(title)
        plt.show()
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
