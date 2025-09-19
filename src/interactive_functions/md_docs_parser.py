from __future__ import annotations

import inspect
from typing import Any

from docstring_parser import DocstringStyle, parse


def doc_to_markdown(obj: Any) -> str:
	"""Render an object's Google/NumPy docstring to Markdown.

	Produces level-2 headers (##) for sections and bullet lists for params.
	"""
	doc = inspect.getdoc(obj) or ""
	ds = parse(doc, style=DocstringStyle.AUTO)

	lines: list[str] = []

	if ds.short_description:
		lines.append(ds.short_description.strip())
		lines.append("")
	if ds.long_description:
		lines.append(ds.long_description.strip())
		lines.append("")

	if ds.params:
		lines.append("## Args")
		for p in ds.params:
			desc = (p.description or "").strip()
			type_prefix = f"({p.type_name}) " if p.type_name else ""
			lines.append(f"- {p.arg_name}: {type_prefix}{desc}")
		lines.append("")

	if ds.returns:
		lines.append("## Returns")
		ret_desc = (ds.returns.description or "").strip()
		if ds.returns.type_name:
			lines.append(f"- {ds.returns.type_name}: {ret_desc}")
		else:
			lines.append(f"- {ret_desc}")
		lines.append("")

	if ds.raises:
		lines.append("## Raises")
		for r in ds.raises:
			tn = r.type_name or "Exception"
			desc = (r.description or "").strip()
			lines.append(f"- {tn}: {desc}")
		lines.append("")

	if ds.examples:
		lines.append("## Examples")
		for ex in ds.examples:
			code = (ex.description or "").strip()
			if code:
				lines.append("```python")
				lines.append(code)
				lines.append("```")
				lines.append("")

	return "\n".join(lines).rstrip()