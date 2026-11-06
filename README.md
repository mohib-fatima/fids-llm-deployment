# Feedback-Induced Distribution Shift in Multilingual LLM Deployment

Mohib Fatima · 2026 (revised November 2026) · Technical Report

Paper: [`paper/FIDS.pdf`](paper/FIDS.pdf)

Zenodo (all versions, always the latest): https://doi.org/10.5281/zenodo.21728188

## Overview

LLMs deployed across many languages can lose quality for underrepresented languages over time while aggregate metrics stay stable. The paper calls this Feedback-Induced Distribution Shift (FIDS) and looks at three mechanisms:

- **Aggregate Masking Effect (AME):** a good overall average hides a bad worst case.
- **Low-Resource Locale Collapse (LRLC):** quality in low-resource languages falls further when feedback and evaluation favor high-resource ones.
- **Aspirational Deferral Lock (ADL):** a scheduler that favors languages already scoring well never gets to the ones that need work.

The paper proves three propositions and a small toy model. RL-Stable Deployment (RLSD) is a design proposal, and its worst-case bound is a conjecture, not a result.

## Empirical illustration (Section 6)

Using NLLB-200 3.3B on FLORES-200 with chrF++, under a synthetic traffic mix:

- Aggregate score 57.03; worst language (Kanuri) 13.54 at 0.105% of traffic.
- High-resource minus low-resource tier gap: 10.79 chrF++ points [95% interval 6.49, 14.74].

Traffic weights are synthetic, so this illustrates the mechanism and does not measure any real deployment.

**Data:** NLLB-200 3.3B dense, FLORES-200 devtest, chrF++, 202 x 201 = 40,602 directions, from github.com/naver/nllb-pruning (`scores/FLORES-devtest-202-3B.tsv`). Language classes: Joshi et al. (2020) taxonomy, microsoft.github.io/linguisticdiversity/assets/lang2tax.txt. FLORES names: github.com/facebookresearch/flores (`flores200/README.md`).

**Run:**
```
python fids_empirical.py FLORES-devtest-202-3B.tsv .
python lrlc_tiers.py FLORES-devtest-202-3B.tsv flores_README.md lang2tax.txt .
```

**Files:** `fids_empirical.py` and `ame_results.json` (aggregate masking, four traffic schemes), `lrlc_tiers.py` and `lrlc_results.json` (resource tiers, bootstrap intervals), `per_language_chrf.tsv` and `lrlc_matched_languages.tsv` (per-language tables).

**Notes**
- The primary traffic scheme was fixed before looking at results. Three other schemes are reported.
- 175 of 201 languages matched the taxonomy by a fixed rule. The unmatched and conflicting codes are listed in `lrlc_results.json`.
- The scores come from a source under CC BY-NC-SA 4.0. The per-language tables are derived from it and carry the same terms. The code can be reused under the repository license.
- chrF++ has script-level biases (Chinese and Japanese score low). See Section 6.3 of the paper.
