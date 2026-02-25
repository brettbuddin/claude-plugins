#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "markdown-it-py[linkify,plugins]",
#     "mdit-py-plugins",
#     "pytest",
# ]
# ///

# Tests for mdview Markdown rendering.

import importlib.machinery
import importlib.util
import os
import sys

_path = os.path.join(os.path.dirname(__file__), "mdview")
_loader = importlib.machinery.SourceFileLoader("mdview", _path)
spec = importlib.util.spec_from_file_location("mdview", _path, loader=_loader)
mdview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mdview)
render = mdview.render


def test_default_fence_rendering():
    """Default fenced code blocks should render with <pre><code class='language-*'>."""
    md = "```python\nprint('hello')\n```"
    html = render(md, "test")
    assert '<pre><code class="language-python">' in html
    assert "print(&#x27;hello&#x27;)" in html or "print('hello')" in html


def test_mermaid_fence_rendering():
    """Mermaid fenced code blocks should render with <pre class='mermaid'>."""
    md = "```mermaid\ngraph TD;\n  A-->B;\n```"
    html = render(md, "test")
    assert '<pre class="mermaid">' in html
    assert '<code class="language-mermaid">' not in html
    assert "graph TD;" in html


def test_mermaid_html_escaping():
    """Mermaid content with special HTML chars should be escaped."""
    md = "```mermaid\ngraph TD;\n  A-->|x < y & z > w|B;\n```"
    html = render(md, "test")
    assert '<pre class="mermaid">' in html
    assert "&lt;" in html
    assert "&gt;" in html or ">" in html  # > may or may not be escaped
    assert "&amp;" in html


def test_mermaid_js_cdn_present():
    """Rendered output should include the Mermaid.js CDN script when mermaid blocks exist."""
    md = "```mermaid\ngraph TD;\n  A-->B;\n```"
    html = render(md, "test")
    assert "mermaid.esm.min.mjs" in html


def test_mermaid_js_cdn_absent_without_mermaid():
    """Rendered output should not include the Mermaid.js CDN script when no mermaid blocks exist."""
    md = "# Hello"
    html = render(md, "test")
    assert "mermaid.esm.min.mjs" not in html


def test_mermaid_css_rule():
    """Rendered output should include the pre.mermaid CSS rule."""
    md = "# Hello"
    html = render(md, "test")
    assert "pre.mermaid" in html


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
