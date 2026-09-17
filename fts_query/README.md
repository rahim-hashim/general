# fts_query

Tiny pure-Python helper that turns user-typed search strings into safe SQLite FTS5 `MATCH` expressions.

## Install

```bash
pip install -e ~/Projects/general/fts_query
```

## Usage

```python
from fts_query import parse

parse("columbia ranking")
# → '"columbia"* "ranking"*'

parse("lakers AND kobe")
# → '"lakers"* AND "kobe"*'

parse('"exact phrase"')
# → '"exact phrase"'

# For consumers whose index does NOT strip periods/apostrophes
# (e.g. metapod's existing atlas.db), disable normalization:
parse("columbia u.s.", normalize_punctuation=False, prefix=False)
# → '"columbia" "u.s."'
```

See `tests/test_parse.py` for the full behavior matrix.
