---
tags:
- remote_sensing
- sentinel_streaming
- streamable
- innovation-summit-2025
---

Sentinel-2 STAC Quicklook Streaming
================
ESIIL, 2024-06-01

This snippet streams a low-resolution overview of Sentinel-2 imagery
using the STAC API and GDAL's `/vsicurl` interface so that no local
GeoTIFF download is required.

We used the following package versions when testing the code:

- requests==2.31.0
- rasterio==1.3.9
- numpy==1.26.4
- pandas==2.2.2
- matplotlib==3.8.4

```python
import json, os, io
from typing import List, Dict, Any, Optional, Tuple
import requests, rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _ensure_ok(r: requests.Response):
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        msg = ""
        try:
            msg = "\nServer says: " + json.dumps(r.json(), indent=2)[:1000]
        except Exception:
            msg = "\nServer says: " + (r.text[:1000] if r.text else "<no body>")
        raise requests.HTTPError(f"{e}{msg}") from None


def search_stac_first_item_resilient(
    stac_api: str,
    collections: List[str],
    datetime_range: str,
    bbox: Optional[List[float]] = None,
    cloud_lt: Optional[float] = 20,
) -> Dict[str, Any]:
    """
    Robust STAC search: try 'query', then no filter, then CQL2-JSON.
    Returns the first Feature; raises if none.
    """
    url = stac_api.rstrip("/") + "/search"
    base = {"collections": collections, "datetime": datetime_range, "limit": 1}
    if bbox is not None:
        base["bbox"] = bbox

    if cloud_lt is not None:
        payload1 = {**base, "query": {"eo:cloud_cover": {"lt": cloud_lt}}}
        r = requests.post(url, json=payload1, timeout=90, headers={"Content-Type": "application/json"})
        if r.status_code < 400:
            _ensure_ok(r)
            feats = r.json().get("features", [])
            if feats:
                return feats[0]

    r = requests.post(url, json=base, timeout=90, headers={"Content-Type": "application/json"})
    if r.status_code < 400:
        _ensure_ok(r)
        feats = r.json().get("features", [])
        if feats:
            return feats[0]

    if cloud_lt is not None:
        payload3 = {
            **base,
            "filter-lang": "cql2-json",
            "filter": {
                "op": "<",
                "args": [
                    {"property": "eo:cloud_cover"},
                    cloud_lt
                ],
            },
        }
        r = requests.post(url, json=payload3, timeout=90, headers={"Content-Type": "application/json"})
        _ensure_ok(r)
        feats = r.json().get("features", [])
        if feats:
            return feats[0]

    _ensure_ok(r)
    raise ValueError("Search succeeded but returned no features for the given parameters.")


def choose_stac_asset(assets: Dict[str, Dict[str, Any]], asset_key: Optional[str] = None) -> Tuple[str, str]:
    if asset_key and asset_key in assets and assets[asset_key].get("href"):
        return asset_key, assets[asset_key]["href"]

    def score(k, a):
        href = (a.get("href") or "").lower()
        roles = [r.lower() for r in a.get("roles", [])]
        t = (a.get("type") or a.get("media_type") or "").lower()
        s = 0
        if "cog" in json.dumps(a).lower() or href.endswith((".tif", ".tiff")):
            s += 5
        if "data" in roles:
            s += 3
        if "image/tiff" in t or "geotiff" in t:
            s += 2
        if k.lower() in ("data", "analytic", "reflectance", "visual", "b04", "b08"):
            s += 1
        return s

    if not assets:
        raise ValueError("STAC item has no assets.")
    key, a = max(assets.items(), key=lambda kv: score(*kv))
    href = a.get("href")
    if not href:
        raise ValueError("Chosen asset has no href.")
    return key, href


def stream_stac_quicklook(
    stac_api: str,
    collection: str,
    datetime_range: str,
    bbox: Optional[List[float]] = None,
    cloud_lt: Optional[float] = 20,
    asset_key: Optional[str] = None,
    overview_level: int = 4,
) -> Tuple[np.ndarray, Dict[str, Any], plt.Figure]:
    item = search_stac_first_item_resilient(stac_api, [collection], datetime_range, bbox=bbox, cloud_lt=cloud_lt)

    item_self = next((l.get("href") for l in item.get("links", []) if l.get("rel") == "self"), None)
    if item_self is None:
        item_self = f"{stac_api.rstrip('/')}/collections/{item.get('collection')}/items/{item.get('id')}"
    r = requests.get(item_self, timeout=90)
    _ensure_ok(r)
    item_full = r.json()

    key, href = choose_stac_asset(item_full.get("assets", {}), asset_key=asset_key)
    vsi_href = f"/vsicurl/{href}" if href.startswith("http") else href

    gdal_env = {
        "AWS_NO_SIGN_REQUEST": os.environ.get("AWS_NO_SIGN_REQUEST", "YES"),
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": os.environ.get("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", "tif,tiff")
    }
    with rasterio.Env(**gdal_env):
        with rasterio.open(vsi_href) as ds:
            if ds.overviews(1):
                olist = ds.overviews(1)
                idx = max(0, min(overview_level - 1, len(olist) - 1))
                out_h = max(1, ds.height // olist[idx])
                out_w = max(1, ds.width // olist[idx])
            else:
                scale = 8 if max(ds.width, ds.height) > 2048 else 2
                out_h = max(1, ds.height // scale)
                out_w = max(1, ds.width // scale)
            arr = ds.read(1, out_shape=(out_h, out_w))
            meta = ds.meta.copy()
            meta.update({"chosen_asset_key": key, "href": href, "vsi_href": vsi_href, "item_id": item.get("id")})

    fig = plt.figure(figsize=(6, 5))
    plt.imshow(arr, interpolation="nearest")
    plt.axis("off")
    plt.title(f"{collection} • {key} • {item.get('id')}")
    plt.tight_layout()
    return arr, meta, fig

```

To fetch a quicklook over Rocky Mountain National Park:

```python
bbox_rmnp = [-105.9, 40.1, -105.3, 40.6]  # west, south, east, north

arr, meta, fig = stream_stac_quicklook(
    stac_api="https://earth-search.aws.element84.com/v1",
    collection="sentinel-2-l2a",
    datetime_range="2024-08-01T00:00:00Z/2024-08-07T23:59:59Z",
    bbox=bbox_rmnp,
    cloud_lt=20,
    asset_key="visual"  # or None
)
fig
```
