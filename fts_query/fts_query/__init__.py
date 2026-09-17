"""Convert user-friendly queries to SQLite FTS5 MATCH expressions.

Vendors metapod's parse_query (webapp/api/main.py:719) and extends it with
optional punctuation normalization and prefix matching toggles.
"""
from __future__ import annotations

__version__ = "0.1.0"

_RESERVED = {"AND", "OR", "NOT"}


def _strip_punct(s: str) -> str:
    """Remove periods and apostrophes. Used when normalize_punctuation=True."""
    return s.replace(".", "").replace("'", "").replace("’", "")


def _expand_hyphens(raw: str, *, prefix: bool) -> str:
    """Wrap a bare term in FTS5 quotes; expand hyphens to an OR clause.

    e.g. 'brain-machine' → '("brain-machine"* OR "brain machine"*)' if prefix.
    """
    clean = raw.strip()
    suffix = "*" if prefix else ""
    if "-" not in clean:
        return f'"{clean}"{suffix}'
    spaced = clean.replace("-", " ")
    return f'( "{clean}"{suffix} OR "{spaced}"{suffix} )'


def _render_phrase(content: str) -> str:
    """Render quoted user input as an FTS5 phrase, expanding hyphen variants.

    Phrases never get prefix suffixes — '"exact phrase"' stays exact.
    """
    content = content.strip()
    if not content:
        return ""
    if "-" in content:
        spaced = content.replace("-", " ")
        return f'( "{content}" OR "{spaced}" )'
    return f'"{content}"'


def parse(
    raw: str,
    *,
    normalize_punctuation: bool = True,
    prefix: bool = True,
) -> str:
    """Convert a user-friendly query into an FTS5 MATCH expression.

    Returns "" if the input is empty or contains only whitespace.

    See README.md and tests/test_parse.py for the full behavior matrix.
    """
    if not raw or not raw.strip():
        return ""

    raw = raw.strip()
    out: list[str] = []
    i = 0
    n = len(raw)
    while i < n:
        c = raw[i]
        if c.isspace():
            i += 1
            continue
        if c in "()":
            out.append(c)
            i += 1
            continue
        if c == '"':
            j = i + 1
            while j < n and raw[j] != '"':
                j += 1
            phrase = raw[i + 1 : j]
            if normalize_punctuation:
                phrase = _strip_punct(phrase)
            rendered = _render_phrase(phrase)
            if rendered:
                out.append(rendered)
            i = j + 1 if j < n else n
            continue
        # Bare token: read until whitespace or paren/quote
        j = i
        while j < n and not raw[j].isspace() and raw[j] not in '()"':
            j += 1
        word = raw[i:j]
        i = j
        if word in _RESERVED:
            out.append(word)
        else:
            if normalize_punctuation:
                word = _strip_punct(word)
            if not word:
                continue
            out.append(_expand_hyphens(word, prefix=prefix))
    return " ".join(out)
