# FIDS Taxonomy

Feedback-Induced Distribution Shift (FIDS) is organized into three primary mechanisms.

| Mechanism | Level | Core dynamic | Potential signal |
|---|---|---|---|
| LEA | Lexical | Model-generated lexical patterns become increasingly represented in future queries | Temporal n-gram frequency and query-distribution divergence |
| LRLC | Locale / population | Feedback dynamics can reinforce weaker adaptation for lower-resource linguistic populations | Locale-level quality and feedback trajectories |
| IAD | Semantic / intent | Users adapt ambiguous query formulations toward the model's preferred intent resolution | Temporal changes in intent distributions |

## 1. Lexical Echo Amplification (LEA)

LEA occurs when model outputs introduce particular lexical patterns — including unusual phrasings, synonym choices, or idiomatic expressions — that users subsequently incorporate into their own queries.

The paper proposes tracking temporal query cohorts and n-gram frequencies as a way to detect this form of distributional change.

## 2. Low-Resource Locale Collapse (LRLC)

LRLC describes a feedback dynamic in which lower reliability for users in low-resource linguistic markets can interact with feedback and adaptation mechanisms to produce further degradation.

The key concern is that aggregate metrics may conceal deterioration affecting populations that contribute relatively small absolute traffic volumes.

## 3. Intent-Anchor Drift (IAD)

IAD is a semantic rather than primarily lexical mechanism.

When model responses consistently resolve ambiguous queries in particular directions, users may progressively adapt how they frame their queries toward those preferred response categories.

## Relationship Between Mechanisms

The three mechanisms operate at different levels:

- **LEA:** surface lexical behavior
- **LRLC:** linguistic-market and population-level behavior
- **IAD:** semantic intent behavior

They are therefore not interchangeable metrics or alternative names for the same phenomenon.

## Evaluation Implication

The taxonomy motivates evaluation that examines not only point-in-time model quality but also longitudinal changes in query distributions and performance across linguistic populations.

A future empirical implementation should explicitly test whether the proposed signatures distinguish FIDS from ordinary distribution shift and other causes of changing user behavior.
