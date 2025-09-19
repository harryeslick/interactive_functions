r"""Dispersal kernels and parameter-bound helper classes.

Provides NumPy-vectorized implementations of common dispersal kernels and
small dataclass wrappers that bind parameters for convenient reuse in plots
and interactive notebooks.

Kernels included:
- Exponential (Laplace in 2D): ``K(r) = exp(-r / \lambda)``
- Gaussian: ``K(r) = exp(-(r / \sigma)^2)``
- Power-law: ``K(r) = (1 + r / \alpha)^{-p}``
- Rectangular hyperbola: ``K(r) = 1 / [1 + (r / \alpha)^p]``
- Exponential-power (Weibull): ``K(r) = exp(-(r / \lambda)^q)``
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .base import BaseFunction

__all__ = [
    "kernel_exponential",
    "kernel_gaussian",
    "kernel_powerlaw",
    "kernel_exppower",
    "kernel_rectangular_hyperbola",
    "ExponentialKernel",
    "GaussianKernel",
    "PowerLawKernel",
    "ExpPowerKernel",
    "RectangularHyperbolaKernel",
]


def _full_nan_like(x: ArrayLike) -> NDArray[np.float64]:
    x_arr = np.asarray(x, dtype=float)
    return np.full_like(x_arr, np.nan, dtype=np.float64)


def kernel_exponential(distance: ArrayLike, lam: float) -> NDArray[np.float64]:
    r"""
    ## Exponential kernel (Laplace in 2D).

    Models short-tailed processes such as rain-splash or gravity drops.

    $K(r) = exp(-r / lam)$

    Args:
        distance: Radial distance ``r`` from the source. Array-like.
        lam: Positive scale parameter (``> 0``).

    Returns:
        Array of shape like ``distance`` with values in ``(0, 1]`` where
        defined; ``NaN`` if ``lam <= 0``.

    Examples:
        >>> import numpy as np
        >>> r = np.linspace(0, 10, 5)
        >>> kernel_exponential(r, lam=2.0).round(4)
        array([1.    , 0.2865, 0.0821, 0.0235, 0.0067])
    """
    if lam <= 0:
        return _full_nan_like(distance)
    r = np.asarray(distance, dtype=float)
    with np.errstate(over="ignore", invalid="ignore"):
        y = np.exp(-r / lam)
    return y.astype(np.float64, copy=False)


def kernel_gaussian(distance: ArrayLike, sigma: float) -> NDArray[np.float64]:
    r"""
    ## Gaussian kernel.

    Suitable for fine aerosols with strong mixing (short tails).

    $K(r) = exp[-(r / sigma)^2]$

    Args:
        distance: Radial distance ``r`` from the source. Array-like.
        sigma: Positive scale (standard deviation-like) parameter (``> 0``).

    Returns:
        Array like ``distance`` with values in ``(0, 1]`` where defined;
        ``NaN`` if ``sigma <= 0``.
    """
    if sigma <= 0:
        return _full_nan_like(distance)
    r = np.asarray(distance, dtype=float)
    with np.errstate(over="ignore", invalid="ignore"):
        y = np.exp(-np.square(r / sigma))
    return y.astype(np.float64, copy=False)


def kernel_powerlaw(distance: ArrayLike, alpha: float, p: float) -> NDArray[np.float64]:
    r"""
    ## Power-law kernel.

    Captures rare long-distance jumps; heavy tails governed by ``p``.

    $K(r) = (1 + r / alpha)^(-p)$

    Args:
        distance: Radial distance ``r`` from the source. Array-like.
        alpha: Positive scale parameter controlling the shoulder (``> 0``).
        p: Positive tail exponent (``> 0``). Larger ``p`` yields shorter tails.

    Returns:
        Array like ``distance`` with values in ``(0, 1]`` where ``1 + r/alpha > 0``;
        ``NaN`` if ``alpha <= 0`` or ``p <= 0``.
    """
    if alpha <= 0 or p <= 0:
        return _full_nan_like(distance)
    r = np.asarray(distance, dtype=float)
    base = 1.0 + r / alpha
    with np.errstate(over="ignore", invalid="ignore"):
        y = np.power(base, -p)
    y = np.where(base > 0.0, y, np.nan)
    return y.astype(np.float64, copy=False)


def kernel_rectangular_hyperbola(
    distance: ArrayLike, alpha: float, p: float
) -> NDArray[np.float64]:
    r"""
    ## Rectangular hyperbola kernel.

    Provides a heavy-tailed form with a softer shoulder compared to
    ``kernel_powerlaw``.

    $K(r) = \dfrac{1}{1 + (r / \alpha)^p}$

    Args:
        distance: Radial distance ``r`` from the source. Array-like.
        alpha: Positive scale parameter controlling the shoulder (``> 0``).
        p: Positive shape parameter (``> 0``). Larger ``p`` steepens decay.

    Returns:
        Array like ``distance`` with values in ``(0, 1]`` where defined;
        ``NaN`` if ``alpha <= 0`` or ``p <= 0``.
    """
    if alpha <= 0 or p <= 0:
        return _full_nan_like(distance)
    r = np.asarray(distance, dtype=float)
    ratio = r / alpha
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        denom = 1.0 + np.power(ratio, p)
        y = np.divide(
            1.0,
            denom,
            out=np.empty_like(ratio, dtype=np.float64),
            where=denom != 0.0,
        )
    y = np.where(denom > 0.0, y, np.nan)
    return y.astype(np.float64, copy=False)


def kernel_exppower(distance: ArrayLike, lam: float, q: float) -> NDArray[np.float64]:
    r"""
    ## Exponential-power (Weibull) kernel.

    Interpolates between Gaussian (``q = 2``) and Exponential (``q = 1``).

    $K(r) = exp[-(r / lam)^q]$

    Args:
        distance: Radial distance ``r`` from the source. Array-like.
        lam: Positive scale parameter (``> 0``).
        q: Positive shape parameter (``> 0``). ``q=2`` approximates Gaussian,
            ``q=1`` reduces to Exponential.

    Returns:
        Array like ``distance`` with values in ``(0, 1]`` where defined;
        ``NaN`` if ``lam <= 0`` or ``q <= 0``.
    """
    if lam <= 0 or q <= 0:
        return _full_nan_like(distance)
    r = np.asarray(distance, dtype=float)
    with np.errstate(over="ignore", invalid="ignore"):
        y = np.exp(-np.power(r / lam, q))
    return y.astype(np.float64, copy=False)


@dataclass(frozen=True)
class ExponentialKernel(BaseFunction):
    r"""Exponential kernel ``K(r) = exp(-r / \lambda)``.

    Binds ``lam`` for convenient reuse in interactive apps.

    Args:
        lam: Positive scale parameter. Default ``10.0``.
    """

    lam: float = 10.0

    MATH_TEMPLATE: ClassVar[str] = r"$K(r) = \exp\!\left(-\dfrac{r}{\lambda}\right)$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:
        return kernel_exponential

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"lam": self.lam}


@dataclass(frozen=True)
class GaussianKernel(BaseFunction):
    r"""Gaussian kernel ``K(r) = exp(-(r / \sigma)^2)``.

    Binds ``sigma`` for convenient reuse in interactive apps.

    Args:
        sigma: Positive scale parameter. Default ``10.0``.
    """

    sigma: float = 10.0

    MATH_TEMPLATE: ClassVar[str] = r"$K(r) = \exp\!\left(-\left(\dfrac{r}{\sigma}\right)^2\right)$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:
        return kernel_gaussian

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"sigma": self.sigma}


@dataclass(frozen=True)
class PowerLawKernel(BaseFunction):
    r"""Power-law kernel ``K(r) = (1 + r / \alpha)^{-p}``.

    Binds ``alpha`` and ``p`` for convenient reuse.

    Args:
        alpha: Positive scale parameter (shoulder). Default ``10.0``.
        p: Positive tail exponent. Default ``2.0``.
    """

    alpha: float = 10.0
    p: float = 2.0

    MATH_TEMPLATE: ClassVar[str] = r"$K(r) = \left(1 + \dfrac{r}{\alpha}\right)^{-p}$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:
        return kernel_powerlaw

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"alpha": self.alpha, "p": self.p}


@dataclass(frozen=True)
class ExpPowerKernel(BaseFunction):
    r"""
    ## Exponential-power kernel 
     
    ``K(r) = exp(-(r / \lambda)^q)``.

    Interpolates between Gaussian (``q=2``) and Exponential (``q=1``).

    Args:
        lam: Positive scale parameter. Default ``10.0``.
        q: Positive shape parameter. Default ``1.5``.
    """

    lam: float = 10.0
    q: float = 1.5

    MATH_TEMPLATE: ClassVar[str] = r"$K(r) = \exp\!\left(-\left(\dfrac{r}{\lambda}\right)^{q}\right)$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:
        return kernel_exppower

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"lam": self.lam, "q": self.q}


@dataclass(frozen=True)
class RectangularHyperbolaKernel(BaseFunction):
    r"""Rectangular hyperbola kernel ``K(r) = 1 / [1 + (r / \alpha)^p]``.

    Binds ``alpha`` and ``p`` for interactive exploration.

    Args:
        alpha: Positive scale parameter. Default ``10.0``.
        p: Positive shape parameter. Default ``2.0``.
    """

    alpha: float = 10.0
    p: float = 2.0

    MATH_TEMPLATE: ClassVar[str] = r"$K(r) = \dfrac{1}{1 + \left(\dfrac{r}{\alpha}\right)^{p}}$"

    @property
    def fn(self) -> Callable[..., NDArray[np.float64]]:
        return kernel_rectangular_hyperbola

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {"alpha": self.alpha, "p": self.p}
