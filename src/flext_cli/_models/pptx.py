"""Private MRO composition for generic PPTX models."""

from __future__ import annotations

from flext_cli import t

from .pptx_presentation import FlextCliModelsPptxPresentation


class FlextCliModelsPptx(FlextCliModelsPptxPresentation):
    """Canonical private PPTX model namespace."""


__all__: t.VariadicTuple[str] = ("FlextCliModelsPptx",)
