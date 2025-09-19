"""Power-law decay function and parameter-bound helper class.

Provides a standalone, NumPy-vectorized implementation and a small
dataclass wrapper that binds parameters for convenient reuse in plots
and interactive notebooks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .base import BaseFunction

__all__ = ["power_law_decay", "PowerLawDecay"]


def power_law_decay(x: ArrayLike, a: float, p: float, b: float) -> NDArray[np.float64]:
    """
    # Power-law decay:
    $f(x) = a * (x + b)^{-p}$

    This shape captures diminishing returns where early increases in ``x``
    have large effects that taper off as ``x`` grows. The domain requires
    ``x + b > 0``; values where this is not satisfied are returned as ``NaN``.

    Args:
        x: Input values. Any array-like structure convertible to ``np.ndarray``.
        a: Positive scale factor controlling the overall height of the curve.
        p: Positive decay exponent; larger values decay faster.
        b: Horizontal shift. The valid domain satisfies ``x + b > 0``.

    Returns:
        A NumPy array ``y`` of the same shape as ``x`` with
        ``y = a * (x + b) ** (-p)`` where valid, and ``NaN`` elsewhere.

    Examples:
        ```python
        import numpy as np
        x = np.linspace(0.1, 10, 5)
        power_law_decay(x, a=2.0, p=1.5, b=0.0).round(4)
        ```
    """
    x_arr = np.asarray(x, dtype=float)
    domain = x_arr + b
    with np.errstate(divide="ignore", invalid="ignore"):
        y = a * np.power(domain, -p)
    y = np.where(domain > 0.0, y, np.nan)
    return y.astype(np.float64, copy=False)


@dataclass(frozen=True)
class PowerLawDecay(BaseFunction):
    """Power-law decay function ``f(x) = a * (x + b)^{-p}``.

    This class binds ``a``, ``p``, and ``b`` parameters for convenient reuse
    in plotting or interactive apps. It evaluates to the same output as the
    standalone :func:`power_law_decay`.

    Args:
        a: Positive scale factor controlling the curve height. Default ``1.0``.
        p: Positive decay exponent; larger values decay faster. Default ``1.0``.
        b: Horizontal shift. Domain requires ``x + b > 0``. Default ``0.0``.

    Notes:
        - Values where ``x + b <= 0`` return ``NaN`` for safe plotting.
        - Computation is fully vectorized and uses ``float64`` outputs.

    Example:
        ```python
        import numpy as np
        from interactive_functions import PowerLawDecay
        f = PowerLawDecay(a=1.5, p=1.0, b=0.0)
        x = np.linspace(0.1, 1.0, 5)
        f(x).round(3)
        f.math_str()
        ```
    """

    a: float = 1.0
    p: float = 1.0
    b: float = 0.0

    # Symbolic template; parameters shown separately via params_str()
    MATH_TEMPLATE: ClassVar[str] = r"$f(x) = a \\cdot (x + b)^{-p}$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:  # -> callable
        return power_law_decay

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"a": self.a, "p": self.p, "b": self.b}
