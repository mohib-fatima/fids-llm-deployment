# FIDS empirical illustration

Rebuilt from the raw scores with two scripts. Section 6 of the paper reports these numbers.

Paper: [`paper/FIDS.pdf`](../paper/FIDS.pdf). Zenodo (all versions, always the latest): https://doi.org/10.5281/zenodo.21728188

**Data:** NLLB-200 3.3B dense, FLORES-200 devtest, chrF++, 202 x 201 = 40,602 directions, from github.com/naver/nllb-pruning (`scores/FLORES-devtest-202-3B.tsv`). Language classes: Joshi et al. (2020) taxonomy, microsoft.github.io/linguisticdiversity/assets/lang2tax.txt. FLORES names: github.com/facebookresearch/flores (`flores200/README.md`).

**Run:**
```
python fids_empirical.py FLORES-devtest-202-3B.tsv .
python lrlc_tiers.py FLORES-devtest-202-3B.tsv flores_README.md lang2tax.txt .
```

**Files:** `fids_empirical.py` and `ame_results.json` (aggregate masking, four traffic schemes), `lrlc_tiers.py` and `lrlc_results.json` (resource tiers, bootstrap intervals), `per_language_chrf.tsv` and `lrlc_matched_languages.tsv` (per-language tables).

**Notes**
- Traffic weights are synthetic. The primary scheme was fixed before looking at results. Three other schemes are reported.
- 175 of 201 languages matched the taxonomy by a fixed rule. The unmatched and conflicting codes are listed in `lrlc_results.json`.
- The scores come from a source under CC BY-NC-SA 4.0. The per-language tables are derived from it and carry the same terms. The code is yours to reuse under the repository license.
- chrF++ has script-level biases (Chinese and Japanese score low). See Section 6.3 of the paper.
