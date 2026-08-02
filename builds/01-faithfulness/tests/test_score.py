"""Unit tests for faithfulness scoring and agreement."""

from faithfulness.metrics import cohens_kappa
from faithfulness.models import ClaimVerdict
from faithfulness.score import compute_faithfulness, is_fully_faithful


def test_score_half():
    verdicts = [
        ClaimVerdict(claim="a", supported=True),
        ClaimVerdict(claim="b", supported=False),
        ClaimVerdict(claim="c", supported=True),
        ClaimVerdict(claim="d", supported=False),
    ]
    assert compute_faithfulness(verdicts) == 0.5


def test_score_full():
    verdicts = [
        ClaimVerdict(claim="a", supported=True),
        ClaimVerdict(claim="b", supported=True),
    ]
    assert compute_faithfulness(verdicts) == 1.0
    assert is_fully_faithful(1.0)


def test_score_empty_is_none():
    assert compute_faithfulness([]) is None
    assert not is_fully_faithful(None)


def test_cohens_kappa_perfect():
    y = [True, False, True, False]
    report = cohens_kappa(y, y)
    assert report.raw_agreement == 1.0
    assert report.cohens_kappa == 1.0


def test_cohens_kappa_deflation_vs_raw():
    """Classic case: high raw agree, lower κ when labels are imbalanced."""
    # 8/10 agree, but mostly False — chance agreement is high
    y_true = [False] * 8 + [True, True]
    y_pred = [False] * 8 + [True, False]
    report = cohens_kappa(y_true, y_pred)
    assert report.raw_agreement == 0.9
    assert report.cohens_kappa < report.raw_agreement
