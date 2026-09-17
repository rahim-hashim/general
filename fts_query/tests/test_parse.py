"""Behavioral tests for fts_query.parse — runs WITHOUT touching SQLite."""
from fts_query import parse


# ── empty / noise ──
def test_empty_returns_empty_string():
    assert parse("") == ""
    assert parse("   ") == ""

def test_whitespace_only_returns_empty():
    assert parse("\t\n  ") == ""


# ── single bare term (defaults: normalize=True, prefix=True) ──
def test_single_bare_term_gets_prefix():
    # Default flags: prefix=True
    assert parse("kobe") == '"kobe"*'


# ── multi-term implicit AND ──
def test_multi_term_implicit_and():
    # FTS5 treats space as implicit AND
    assert parse("lakers kobe") == '"lakers"* "kobe"*'


# ── explicit boolean operators ──
def test_explicit_and():
    assert parse("lakers AND kobe") == '"lakers"* AND "kobe"*'

def test_explicit_or():
    assert parse("lakers OR celtics") == '"lakers"* OR "celtics"*'

def test_explicit_not():
    assert parse("lakers NOT celtics") == '"lakers"* NOT "celtics"*'

def test_lowercase_operators_are_treated_as_terms():
    # Only uppercase AND/OR/NOT are operators
    assert parse("lakers and kobe") == '"lakers"* "and"* "kobe"*'


# ── parentheses ──
def test_parentheses_preserved():
    assert parse("(lakers AND kobe) OR celtics") == \
        '( "lakers"* AND "kobe"* ) OR "celtics"*'


# ── quoted phrases ──
def test_quoted_phrase_no_prefix():
    # Phrases get no trailing *
    assert parse('"exact phrase"') == '"exact phrase"'

def test_quoted_phrase_with_other_terms():
    assert parse('"new york" times') == '"new york" "times"*'


# ── hyphen expansion ──
def test_hyphen_expands_to_or_clause():
    assert parse("brain-machine") == \
        '( "brain-machine"* OR "brain machine"* )'

def test_hyphen_in_quoted_phrase_expands():
    assert parse('"brain-computer interface"') == \
        '( "brain-computer interface" OR "brain computer interface" )'


# ── normalize_punctuation (default True) ──
def test_normalize_strips_periods_in_bare_terms():
    # 'U.S.' → 'us' → "us"*
    assert parse("U.S.") == '"US"*'  # case preserved by parser; FTS5 unicode61 case-folds
    # More realistic check:
    assert parse("u.s.") == '"us"*'

def test_normalize_strips_periods_in_dotted_abbreviations():
    assert parse("e.g.") == '"eg"*'

def test_normalize_strips_apostrophes_in_possessives():
    assert parse("Columbia's") == '"Columbias"*'

def test_normalize_strips_curly_apostrophe():
    # Unicode right single quote (U+2019) — common from word processors
    assert parse("Columbia's") == '"Columbias"*'

def test_normalize_in_quoted_phrase():
    assert parse('"U.S. News"') == '"US News"'

def test_normalize_columbia_us_full_query():
    # The canonical bug repro: 'columbia u.s.' must produce two real tokens
    assert parse("columbia u.s.") == '"columbia"* "us"*'


# ── normalize_punctuation=False (metapod compatibility) ──
def test_no_normalize_preserves_periods():
    assert parse("u.s.", normalize_punctuation=False) == '"u.s."*'

def test_no_normalize_preserves_apostrophe():
    assert parse("Columbia's", normalize_punctuation=False) == \
        '"Columbia\'s"*'

def test_metapod_compatibility_mode():
    # normalize_punctuation=False + prefix=False = original metapod parse_query
    assert parse("lakers kobe", normalize_punctuation=False, prefix=False) == \
        '"lakers" "kobe"'


# ── empty-after-strip edge cases ──
def test_lone_period_disappears():
    # '.' alone becomes '' after stripping; should be dropped, not produce '""*'
    assert parse(".") == ""

def test_lone_apostrophe_disappears():
    assert parse("'") == ""


# ── prefix toggle ──
def test_prefix_default_on_for_bare_terms():
    assert parse("thad") == '"thad"*'

def test_prefix_off_for_bare_terms():
    assert parse("thad", prefix=False) == '"thad"'

def test_prefix_never_on_phrases():
    assert parse('"exact phrase"') == '"exact phrase"'
    assert parse('"exact phrase"', prefix=False) == '"exact phrase"'

def test_prefix_off_no_trailing_star_anywhere():
    assert parse("lakers AND kobe", prefix=False) == \
        '"lakers" AND "kobe"'

def test_prefix_on_hyphen_expansion():
    assert parse("brain-machine") == \
        '( "brain-machine"* OR "brain machine"* )'
    assert parse("brain-machine", prefix=False) == \
        '( "brain-machine" OR "brain machine" )'
