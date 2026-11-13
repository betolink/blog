---
title: "A small numerical check: orbital period from Kepler's third law"
date: 2026-11-10T14:30:00-06:00
description: "A short worked example with equations, a table, and Python code."
tags: ["python", "physics", "numerical-methods"]
categories: ["science"]
math: true
draft: false
---

Kepler's third law relates the orbital period \(T\) to the semi-major axis \(a\)
for a body orbiting a mass \(M\):

$$
T = 2\pi \sqrt{\frac{a^3}{GM}}.
$$

For Earth around the Sun, using \(a = 1.496 \times 10^{11}\,\mathrm{m}\) and
\(GM = 1.327 \times 10^{20}\,\mathrm{m^3\,s^{-2}}\), we expect roughly one year.

```python
import math

GM = 1.32712440018e20
a = 1.495978707e11

period_seconds = 2 * math.pi * math.sqrt(a**3 / GM)
print(period_seconds / (365.25 * 24 * 3600))
```

```text
1.0000
```

## Reference values

| Body | Semi-major axis (AU) | Period (years) |
|---|---:|---:|
| Mercury | 0.387 | 0.241 |
| Earth | 1.000 | 1.000 |
| Mars | 1.524 | 1.881 |
| Jupiter | 5.203 | 11.862 |

The point is not the arithmetic. The point is that a notebook can carry the
claim, the code, and the output together.
