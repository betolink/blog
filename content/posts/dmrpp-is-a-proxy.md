---
title: "dmrpp as a chunk reference format"
date: 2026-11-12T11:00:00-06:00
description: "A short note on DMR++ sidecars, virtual chunk manifests, and the integrity gap between a reference and the file it points at."
tags: ["dmrpp", "zarr", "icechunk", "virtualizarr", "metadata", "earth-observation"]
categories: ["data-systems"]
draft: false
---

I keep coming back to DMR++. It is a good old idea: instead of making every
client parse an HDF5 granule from scratch, publish the map ahead of time. A
sidecar gives you dimensions, variables, chunk positions, offsets, and byte
lengths. The client follows the references and only fetches what it needs.

That is a proxy. It is not a copy, and it is not a proof.

The [reference notebook]({{< relref "/notebooks/dmrpp-to-zarr" >}}) parses a
small DMR++ document, turns the offsets into a VirtualiZarr chunk manifest, and
puts the result next to an Icechunk-style manifest.

## Old ideas come back again

At the chunk level, DMR++ and an Icechunk manifest are basically the same kind
of object. Both say: this chunk lives in this file at this offset for this many
bytes. Both let you build a virtual array without copying data.

The difference is ownership. A DMR++ file sits next to a granule. An Icechunk
manifest lives inside a versioned store snapshot with transactional semantics.
One is a static map. The other is a map with a lifecycle.

A healthy DMR++ ecosystem is still worth having. Aggregated virtual cubes should
live in Icechunk, but DMR++ can help assemble them when the sidecars are current,
avoiding another round of heavy granule parsing. And not every dataset wants to
be a rectilinear cube: EMIT and other multispectral products are awkward to fit
into one regular array. Even when they are not Icechunkable, DMR++ references to
individual files still make it cheap to pull specific hyperspectral bands and
load them lazily.

## DMR++ lacks a file checksum

DMR++ tells you where to read. It does not hash-bind the reference to the file
it points at. If the granule is regenerated or replaced, an old sidecar can
still point into a valid object and hand you the wrong bytes. You cannot tell
that from the reference alone before reading.

So treat DMR++ as an access and caching layer, not an integrity layer. If you
need to know the reference is current, use immutable object names or object
versioning, a checksum or ETag at the storage layer, a sidecar regeneration
step, or a store that records the reference and object version together.

## Where it comes from

The underlying move is older than cloud-native formats. The
[HDF4MapReader](https://hdf4mapreader.sourceforge.net/index.html) project, which
I was involved with, exposed the internal metadata of scientific files so people
could still understand them years after the original tools disappeared.

DMR++ and virtual chunk manifests are the same instinct, just more operational:
make the internal map explicit, portable, and useful to software other than the
original reader. The map should outlive the program that wrote the file. It
still needs something else to prove the map is current.
