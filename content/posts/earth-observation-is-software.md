---
title: "Earth observation data is a software problem"
date: 2026-11-05T09:15:00-06:00
description: "Notes on cloud-native formats, metadata, and the engineering work that makes scientific data usable."
tags: ["earth-observation", "data-systems", "zarr", "cloud"]
categories: ["science"]
draft: false
---

Earth observation archives are often described as data problems. In practice,
most of the friction is software: metadata that does not agree with itself,
formats that require whole-file downloads, and access patterns that assume a
local filesystem.

## What cloud-native changes

Chunked, self-describing arrays make partial reads practical. A workflow can
open a dataset, inspect coordinates, and request one time slice without
downloading the archive.

```python
import xarray as xr

ds = xr.open_zarr(
    "https://example.com/store.zarr",
    consolidated=True,
    chunks={},
)
print(ds)
```

The hard part is not the API. The hard part is consistency across collections,
clear provenance, and clients that fail gracefully.

## A short checklist

- Does the dataset expose stable, documented dimensions and coordinates?
- Can a user discover the variables without downloading the whole object?
- Are missing values and scale factors handled explicitly?
- Is there a small, runnable example in the documentation?

Those questions sound mundane. They are also the difference between an archive
that is technically online and one that is actually usable.
