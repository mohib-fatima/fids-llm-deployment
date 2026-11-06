# Research Overview

## Motivation

Large language models deployed in multilingual production environments are typically evaluated using benchmarks and point-in-time aggregate metrics. These evaluation approaches were largely designed before iterative, feedback-driven deployment became the norm, and they are poorly suited to detect a specific class of failure: gradual, locale-specific quality degradation that persists precisely because it does not show up in the metrics teams are watching.

This project is motivated by production-scale observations from large-scale multilingual AI deployment, where this pattern recurred across different systems and product areas in structurally similar ways. Feedback-Induced Distribution Shift (FIDS) is the attempt to name, formalize, and propose mitigations for that pattern.

## What FIDS Is

FIDS describes a systems-level failure in which design and evaluation choices, not model limitations, allow localized quality declines to persist while aggregate metrics remain stable. The paper characterizes three specific mechanisms through which this happens: the Aggregate Masking Effect, the Aspirational Deferral Lock, and Low-Resource Locale Collapse. Full definitions are in [fids-taxonomy.md](fids-taxonomy.md).

## What FIDS Is Not

FIDS is not a claim about any specific deployed system's current internal metrics. It is a formal characterization of structural failure modes, grounded in production experience, with proofs under stated assumptions. The paper includes an empirical illustration on public data (NLLB-200 on FLORES-200, Section 6), but the traffic weights in it are synthetic, so it shows the mechanism and does not measure a real deployment. Other numeric examples in the paper are labeled as illustrative, not as measured findings.

## RL-Stable Deployment (RLSD)

The paper proposes RLSD as a response to these failure modes: an inference-time adaptation framework where a reinforcement learning controller observes production telemetry and selects targeted interventions, without requiring model retraining. RLSD is a design proposal. It has not been implemented at production scale in this repository. The paper states its worst-case stability bound as a conjecture, with a toy special case worked out.

## Open Research Questions

- How can locale-level quality degradation be detected reliably without disaggregated monitoring infrastructure that many production systems do not currently have?
- How should prioritization and resourcing rules be redesigned to avoid structurally locking out low-traffic or low-resource segments, as described by the Aspirational Deferral Lock?
- What telemetry signals are reliable enough, and resistant enough to gaming, to serve as the reward signal for an adaptation framework like RLSD?
- How should multilingual LLM evaluation frameworks incorporate locale-level and temporal trajectories, rather than relying solely on point-in-time aggregate scores?
- What is the relationship between FIDS and other feedback-loop phenomena documented in the broader machine learning literature (see the paper's related work section)?

## Relationship to the Author's Second Paper

A related but distinct project, on engagement-accuracy decoupling in LLM-mediated search (Triangulation Collapse), is a separate preprint: https://doi.org/10.5281/zenodo.22182821. Its code and data are at https://github.com/mohib-fatima/tc-paper. Both projects share a common thread: ordinary optimization processes (aggregate averaging in FIDS, engagement-based ranking in the search paper) producing predictable, structural harm without any single actor making an obviously bad decision.

## Status

This is an active, independent research project. The paper is a preprint on Zenodo (all versions: https://doi.org/10.5281/zenodo.21728188). See the main [README](../README.md) for the paper and data.
