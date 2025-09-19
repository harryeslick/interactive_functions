"""Base abstractions for parameter-bound mathematical functions.

Provides an abstract base class with default implementations for calling a
standalone vectorized function and generating a LaTeX math string for titles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar, Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

__all__ = ["BaseFunction"]


def _value(v: Any) -> float:
    """Extract a numeric value from ``v``.

    Supports plain numbers as well as objects with a ``.value`` attribute
    (e.g., marimo/ipywidgets sliders). This makes the classes convenient to
    use in interactive notebooks without extra glue code.
    """

    raw = getattr(v, "value", v)
    try:
        return float(raw)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"Cannot convert {type(v)!r} to float; expected a number or an object with .value"
        ) from exc


class BaseFunction(ABC):
    r"""ABC for simple parameter-bound mathematical functions.

    Subclasses should define:
    - ``fn``: a callable with signature ``fn(x, **parameters) -> np.ndarray``
    - ``parameters``: a mapping of parameter names to values
    - ``MATH_TEMPLATE`` (ClassVar[str]): a symbolic LaTeX string using variable
      names (e.g., ``$f(x) = a \cdot \ln(x + b)$``) — not a format string.

    The default ``__call__`` delegates to ``fn(x, **parameters)``. ``math_str``
    returns the symbolic expression unchanged, while ``params_str`` renders a
    separate compact string of parameter values like ``"a=1.00, b=2.00"``.
    """

    # Symbolic LaTeX template for the function (with variable names).
    MATH_TEMPLATE: ClassVar[str] = ""

    @property
    @abstractmethod
    def fn(self) -> Callable[..., NDArray[np.float64]]:
        """Return the standalone function implementing the formula."""

    @property
    @abstractmethod
    def parameters(self) -> Mapping[str, Any]:
        """Return a mapping of parameter names to values (numbers or widget-like)."""

    def __call__(self, x: ArrayLike) -> NDArray[np.float64]:
        """Evaluate the function for array-like ``x`` with bound parameters."""

        # Extract primitives in case values are widget-like (have .value)
        params = {k: _value(v) for k, v in self.parameters.items()}
        return self.fn(x, **params)

    def math_str(self) -> str:
        """Return the symbolic LaTeX string for the function.

        This returns ``MATH_TEMPLATE`` unchanged (with variable names), not
        formatted with parameter values.
        """

        return self.MATH_TEMPLATE

    def params_str(self, precision: int = 2, sep: str = ", ") -> str:
        """Return a compact string of parameter values, e.g., ``"a=1.23, b=2.00"``.

        Args:
            precision: Number of decimal places for floating-point formatting.
            sep: Separator between ``key=value`` pairs.

        Returns:
            A string of comma-separated ``key=value`` pairs.
        """

        items: list[str] = []
        for k, v in self.parameters.items():
            val = _value(v)
            items.append(f"{k}={val:.{precision}f}")
        return sep.join(items)
