"""Logarithmic growth function and parameter-bound helper class.

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

__all__ = ["log_growth", "LogGrowth"]


def log_growth(x: ArrayLike, a: float, b: float) -> NDArray[np.float64]:
    r"""
    # Logarithmic growth
    $f(x) = a * \ln(x + b)$

    Models growth with diminishing marginal gains. The domain requires
    ``x + b > 0``; values where this condition is not satisfied are
    returned as ``NaN`` to make plotting safe.

    Args:
        x: Input values. Any array-like structure convertible to ``np.ndarray``.
        a: Scale factor controlling the vertical stretch of the curve.
        b: Horizontal shift; ensures the argument of ``ln`` remains positive.

    Returns:
        A NumPy array ``y`` of the same shape as ``x`` with
        ``y = a * np.log(x + b)`` where valid, and ``NaN`` elsewhere.

    Examples:
        ```python
        import numpy as np
        x = np.array([0.1, 1.0, 2.0])
        log_growth(x, a=1.5, b=1.0).round(4)
        ```
    """
    x_arr = np.asarray(x, dtype=float)
    domain = x_arr + b
    with np.errstate(divide="ignore", invalid="ignore"):
        y = a * np.log(domain)
    y = np.where(domain > 0.0, y, np.nan)
    return y.astype(np.float64, copy=False)


@dataclass(frozen=True)
class LogGrowth(BaseFunction):
    """Logarithmic growth function ``f(x) = a * ln(x + b)``.

    This class binds ``a`` and ``b`` for convenient reuse, and evaluates to
    the same output as :func:`log_growth`.

    Args:
        a: Vertical scale factor. Default ``1.0``.
        b: Horizontal shift. Domain requires ``x + b > 0``. Default ``1.0``.

    Notes:
        - Values where ``x + b <= 0`` return ``NaN`` for safe plotting.
        - Computation is fully vectorized and uses ``float64`` outputs.

    Example:
        ```python
        import numpy as np
        from interactive_functions import LogGrowth
        g = LogGrowth(a=2.0, b=1.0)
        x = np.array([0.1, 1.0, 3.0])
        g(x).round(3)
        g.math_str()
        ```
    """

    a: float = 1.0
    b: float = 1.0

    MATH_TEMPLATE: ClassVar[str] = r"$f(x) = a \\cdot \\ln(x + b)$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:  # -> callable
        return log_growth

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"a": self.a, "b": self.b}
