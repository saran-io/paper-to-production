# Faithfulness datasets

| Path | Purpose |
|---|---|
| `fixtures/seed_cases.json` | CI + regression (8 cases, all buckets) |
| `fixtures/labelled_v1.json` | Expanded labelled set (~53) from listings |
| `../listings/` | 30 property listing docs (`listing_01.txt` … + `manifest.json`) |

## Label taxonomy (ADR-001)

fully_supported · partially_supported · contradictory · correct_but_unsupported · poor_retrieval · wrong_price_or_feature · facts_merged_across_properties · empty_retrieval

## Target

≥75 hand-verified cases before publish. `labelled_v1.json` is the working set — spot-check generated labels before trusting κ in the blog.
