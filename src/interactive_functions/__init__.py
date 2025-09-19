"""Playground for viewing mathematical functions.

This package contains interactive examples and helpers for plotting
mathematical functions. See docs for marimo apps and examples.
"""

from __future__ import annotations

# Re-export core functions and helper classes
from .base import BaseFunction
from .dispersal_kernels import (
	ExponentialKernel,
	ExpPowerKernel,
	GaussianKernel,
	PowerLawKernel,
	RectangularHyperbolaKernel,
	kernel_exponential,
	kernel_exppower,
	kernel_gaussian,
	kernel_powerlaw,
	kernel_rectangular_hyperbola,
)
from .log_growth import LogGrowth, log_growth
from .power_law_decay import PowerLawDecay, power_law_decay

__version__ = "0.1.0"

__all__ = [
	"__version__",
	"power_law_decay",
	"log_growth",
	"PowerLawDecay",
	"LogGrowth",
	"BaseFunction",
	# Dispersal kernels
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
