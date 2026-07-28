"""Agreement metrics — headline is Cohen's κ, not raw agreement."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgreementReport:
    n: int
    raw_agreement: float
    cohens_kappa: float
    both_true: int
    both_false: int
    pred_true_human_false: int
    pred_false_human_true: int


def cohens_kappa(y_true: list[bool], y_pred: list[bool]) -> AgreementReport:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be the same length")
    if not y_true:
        raise ValueError("need at least one label pair")

    n = len(y_true)
    tt = tf = ft = ff = 0
    for t, p in zip(y_true, y_pred, strict=True):
        if t and p:
            tt += 1
        elif t and not p:
            ft += 1
        elif not t and p:
            tf += 1
        else:
            ff += 1

    raw = (tt + ff) / n
    # Marginal probabilities
    p_true_t = (tt + ft) / n
    p_true_p = (tt + tf) / n
    p_false_t = (ff + tf) / n
    p_false_p = (ff + ft) / n
    pe = p_true_t * p_true_p + p_false_t * p_false_p
    kappa = 1.0 if pe == 1.0 else (raw - pe) / (1.0 - pe)

    return AgreementReport(
        n=n,
        raw_agreement=raw,
        cohens_kappa=kappa,
        both_true=tt,
        both_false=ff,
        pred_true_human_false=tf,
        pred_false_human_true=ft,
    )
