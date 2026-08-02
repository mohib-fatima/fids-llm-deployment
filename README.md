# Feedback-Induced Distribution Shift in Multilingual LLM Deployment

Research repository accompanying:

**Feedback-Induced Distribution Shift in Multilingual LLM Deployment: Evidence, Characterization, and RL-Based Adaptation Strategies**

**Mohib Fatima · 2026 · Technical Report**

[Read the paper on Zenodo](https://doi.org/10.5281/zenodo.21728189) ·
[DOI: 10.5281/zenodo.21728189](https://doi.org/10.5281/zenodo.21728189)

---

## Overview

Large language models deployed across multilingual production environments often experience performance degradation for underrepresented languages over time. This paper identifies this phenomenon as **Feedback-Induced Distribution Shift (FIDS)**, a systems-level failure in which design and evaluation choices allow localized quality declines to persist while aggregate metrics remain stable.

Drawing on production-scale experience in multilingual LLM deployment, the paper characterizes three recurring patterns through which these failures emerge, gives each pattern a formal proof-backed guarantee, and shows that standard benchmarking approaches are poorly suited to detect them. It also introduces **RL-Stable Deployment (RLSD)**, a reinforcement-learning-based framework that dynamically adapts inference policies in response to performance signals, without requiring model retraining.

For the full taxonomy and mechanism details, see [docs/fids-taxonomy.md](docs/fids-taxonomy.md).
For project motivation, scope, and open research questions, see [docs/research-overview.md](docs/research-overview.md).

## FIDS Taxonomy (summary)

1. **Aggregate Masking Effect (AME)** — locale-level quality regressions get averaged away by aggregate dashboards, so the top-line metric looks stable while specific segments quietly degrade.
2. **Aspirational Deferral Lock (ADL)** — once a metric crosses an acceptable threshold, the backlog behind it stops getting revisited; the deferral becomes permanent by default, not by decision.
3. **Low-Resource Locale Collapse (LRLC)** — locales that start under-resourced get deprioritized every cycle for the same structural reason, compounding into progressively worse degradation over time.

Full definitions, formal propositions, and proofs are in the paper and in [docs/fids-taxonomy.md](docs/fids-taxonomy.md).

## RL-Stable Deployment (RLSD)

RLSD is proposed as an inference-time adaptation framework: an RL controller observes production telemetry and selects targeted interventions in response to detected FIDS signals, without requiring model retraining. RLSD is presented as a research framework and theoretical proposal; this repository does not claim a production-scale implementation or controlled empirical validation.

## Evidence and Scope

The FIDS framework is motivated by production-scale observations from multilingual LLM deployment and grounded in formal analysis. This repository does not claim:

- a controlled randomized evaluation of FIDS;
- a production-scale implementation of RLSD;
- a validated benchmark suite; or
- empirical proof that the proposed adaptation framework improves user outcomes.

These are identified as future work in the paper's limitations section.

## Repository Structure

```text
fids-llm-deployment/
│
├── README.md                    (this file)
│
├── paper/
│   ├── FIDS.pdf
│   └── README.md                (paper metadata and citation)
│
├── docs/
│   ├── research-overview.md     (motivation, scope, research questions)
│   └── fids-taxonomy.md         (full taxonomy detail)
│
└── LICENSE                      (CC BY 4.0)
```

## Citation

```
Fatima, M. (2026). Feedback-Induced Distribution Shift in Multilingual LLM
Deployment: Evidence, Characterization, and RL-Based Adaptation Strategies.
Zenodo. https://doi.org/10.5281/zenodo.21728189
```

## Contact

Mohib Fatima · mohib.fatima.edu@gmail.com · [ORCID](https://orcid.org/0009-0009-4138-7698)
