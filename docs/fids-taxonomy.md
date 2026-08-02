# FIDS Taxonomy

Feedback-Induced Distribution Shift (FIDS) is characterized in the paper as three related but distinct failure patterns. Each is given a formal proposition and proof in the paper; this document summarizes the mechanism and intuition behind each one in plain language.

---

## 1. Aggregate Masking Effect (AME)

**Mechanism:** When a system's overall quality metric is computed as a traffic-weighted average across locales, a small number of high-traffic locales dominate that average. A significant quality regression in a lower-traffic locale can be mathematically invisible in the aggregate number, even though it represents a real, sometimes severe, degradation for the affected users.

**Why it matters:** Dashboards and alerting systems built on aggregate metrics will not fire, and the responsible team will have no signal that anything is wrong, because nothing in the number they're watching has changed.

**Formal characterization:** The paper proves a bound showing that an aggregate quality alert cannot fire, regardless of how severe the underlying degradation is, whenever a locale's traffic weight falls below a threshold set by the alert sensitivity. This means the failure to detect is not a tuning problem; it is a structural property of computing quality as a single traffic-weighted average.

---

## 2. Aspirational Deferral Lock (ADL)

**Mechanism:** Engineering and product teams allocate attention using some prioritization rule, often implicitly weighting locales or issues by current traffic or visible impact. Once an issue or locale falls below the threshold that rule uses to allocate attention, it stops receiving attention in every subsequent cycle, for the same structural reason. The backlog does not shrink through neglect; it is what the allocation rule produces by construction.

**Why it matters:** This is not a failure of judgment or prioritization discipline. It is what happens by default whenever attention is allocated by a rule that assigns zero weight to a category, regardless of how much cumulative harm sits in that category.

**Formal characterization:** The paper shows that under greedy allocation with a zero-weight objective for a given locale or issue class, the backlog for that class persists indefinitely as a direct consequence of the allocation rule's structure, independent of the backlog's actual size or severity. The mechanism only breaks if the weighting function is changed to account for factors like backlog age or coverage, not traffic alone.

---

## 3. Low-Resource Locale Collapse (LRLC)

**Mechanism:** Locales that start with less annotation investment, less human review capacity, or less engineering attention tend to receive less of all three in every subsequent cycle, because the same resourcing decisions that created the initial gap keep getting made the same way. As engagement in the locale drops due to poor quality, the data signals available for improving that locale also shrink, compounding the original disadvantage.

**Why it matters:** This produces a self-reinforcing cycle: quality issues are not just persistent but actively compounding, and the mechanism means that identical starting gaps can grow rather than close over time even without any single deliberate decision to deprioritize the locale.

**Formal characterization:** The paper models this as a discrete-time recursion, showing that under the stated conditions, per-locale quality degrades toward a fixed point that is strictly worse than the starting condition, driven by the interaction between reduced human annotation capacity and reduced engagement-derived data signals.

---

## Relationship Between the Three Patterns

AME explains why the problem stays *invisible* to standard monitoring. ADL explains why, even when visible, the problem stays *unaddressed* by standard prioritization. LRLC explains why the problem *compounds* rather than remains static once it exists. Together they describe a full lifecycle: a degradation emerges, gets masked from detection, fails to get prioritized even if noticed, and compounds over time in exactly the locales least equipped to absorb it.

## Note on Scope

These three patterns are formalized as proven consequences of stated structural assumptions (how aggregate metrics are computed, how greedy allocation rules behave, how annotation capacity interacts with engagement). They are not presented as claims about any specific company's internal systems, and the paper's simulation and illustrative sections are explicitly labeled as such, not as empirical measurements. See the paper's Limitations section for a full discussion of scope.
