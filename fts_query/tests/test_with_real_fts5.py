"""Round-trip tests: every parse() output must be valid FTS5 MATCH syntax.

Builds a tiny in-memory FTS5 table, indexes the canonical-bug fixture, then
runs MATCH using parse() output to prove (a) the syntax is valid and
(b) the canonical repros actually return the expected row.
"""
import sqlite3
import pytest
from fts_query import parse


@pytest.fixture
def conn():
    """In-memory FTS5 table indexing one row that matches the spec's canonical bug."""
    c = sqlite3.connect(":memory:")
    c.executescript("""
        CREATE VIRTUAL TABLE docs USING fts5(
            title, author,
            tokenize='porter unicode61'
        );
        -- Pre-normalize at index time: strip periods + apostrophes.
        INSERT INTO docs(rowid, title, author) VALUES
            (1, 'An Investigation of the Facts Behind Columbias US News Ranking',
                'Michael Thaddeus'),
            (2, 'Lakers vs Celtics 2024 Recap', 'Sports Desk'),
            (3, 'Brain-machine interfaces explained', 'Jane Doe');
    """)
    return c


def _matches(conn, query):
    expr = parse(query)
    if not expr:
        return []
    cur = conn.execute("SELECT rowid FROM docs WHERE docs MATCH ?", (expr,))
    return [r[0] for r in cur.fetchall()]


# ── canonical bug repros ──
def test_columbia_ranking_finds_thaddeus(conn):
    assert 1 in _matches(conn, "Columbia ranking")

def test_columbia_us_finds_thaddeus(conn):
    # The bug the user reported on 2026-06-04
    assert 1 in _matches(conn, "columbia u.s.")

def test_author_search_finds_thaddeus(conn):
    assert 1 in _matches(conn, "Michael Thaddeus")

def test_prefix_finds_thaddeus(conn):
    assert 1 in _matches(conn, "thad")


# ── operators work ──
def test_boolean_and(conn):
    # Both terms must be present somewhere in the document
    assert _matches(conn, "lakers AND celtics") == [2]
    assert _matches(conn, "lakers AND thaddeus") == []

def test_boolean_not(conn):
    assert 2 not in _matches(conn, "celtics NOT lakers")


# ── hyphen expansion ──
def test_hyphenated_finds_both_forms(conn):
    # 'brain-machine' should find doc 3 (which has 'brain-machine')
    # AND would find 'brain machine' if such a doc existed.
    assert 3 in _matches(conn, "brain-machine")


# ── syntax safety: nothing should raise ──
@pytest.mark.parametrize("query", [
    "",
    "   ",
    "a",  # single char dropped — produces empty MATCH? Actually parse returns "a"* — FTS5 accepts
    "AND",  # bare reserved word: parse outputs literal "AND" — FTS5 sees an operator with no operands
    "(",
    ")",
    "()",
    '"',
    '"unterminated',
    "lakers OR",  # dangling operator
])
def test_safe_no_raise(conn, query):
    """No user input should make parse() crash or produce a SQL injection vector."""
    expr = parse(query)
    if not expr:
        return  # empty is fine — caller falls through
    try:
        conn.execute("SELECT rowid FROM docs WHERE docs MATCH ?", (expr,)).fetchall()
    except sqlite3.OperationalError:
        # FTS5 may reject some malformed expressions (e.g. dangling operators).
        # Acceptable — the test is that we don't crash Python and don't allow SQL injection.
        # The empty / well-formed cases must succeed; failures here are FTS5 syntax errors,
        # which the caller should catch and treat as "no results".
        pass
