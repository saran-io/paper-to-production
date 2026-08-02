"""Decomposition and verification unit tests."""

from faithfulness.decompose import HeuristicDecomposer, ScriptedDecomposer
from faithfulness.models import Claim
from faithfulness.verify import HeuristicVerifier, ScriptedVerifier


def test_heuristic_decompose_splits_and():
    d = HeuristicDecomposer()
    claims = d.decompose(
        "Tell me about 4B",
        "Unit 4B is priced at ₹1.8 Cr and includes a gym.",
    )
    texts = [c.text.lower() for c in claims]
    assert len(claims) >= 2
    assert any("1.8" in t or "1.8" in t.replace(" ", "") for t in texts)
    assert any("gym" in t for t in texts)


def test_heuristic_decompose_empty():
    assert HeuristicDecomposer().decompose("q", "") == []
    assert HeuristicDecomposer().decompose("q", "   ") == []


def test_scripted_decompose():
    d = ScriptedDecomposer({"Hello.": ["A", "B"]})
    claims = d.decompose("q", "Hello.")
    assert [c.text for c in claims] == ["A", "B"]


def test_heuristic_verify_wrong_price():
    v = HeuristicVerifier()
    verdict = v.verify(
        Claim(text="Unit 4B is priced at ₹1.8 Cr"),
        ["Unit 4B is a 2BHK apartment priced at ₹1.2 Cr. It includes pool access."],
    )
    assert verdict.supported is False


def test_heuristic_verify_supported_pool():
    v = HeuristicVerifier()
    verdict = v.verify(
        Claim(text="It includes pool access"),
        ["Unit 4B is a 2BHK apartment priced at ₹1.2 Cr. It includes pool access."],
    )
    assert verdict.supported is True


def test_scripted_verifier():
    v = ScriptedVerifier({"claim a": True, "claim b": False})
    assert v.verify(Claim(text="Claim A"), []).supported is True
    assert v.verify(Claim(text="Claim B"), []).supported is False
