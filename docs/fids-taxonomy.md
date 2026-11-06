# FIDS Taxonomy

Feedback-Induced Distribution Shift (FIDS) is characterized in the paper as three related but distinct failure patterns. Each is given a formal proposition in the paper (Propositions 1 to 3); this document summarizes the mechanism and intuition behind each one in plain language.

---

## 1. Aggregate Masking Effect (AME), Proposition 1

**Mechanism:** When a system's overall quality metric is computed as a traffic-weighted average across locales, high-traffic locales dominate that average. A significant quality regression in a lower-traffic locale can barely move the aggregate number, even though it is a real, sometimes severe, degradation for the affected users.

**Why it matters:** Dashboards and alerts built on the aggregate will not fire when the condition below holds, and the responsible team gets no signal that anything is wrong, because nothing in the number they are watching has changed.

**Formal characterization:** Proposition 1 shows that an aggregate alert cannot fire whenever δ_max · w_S < Q_before − τ, that is, whenever the affected locales' traffic share w_S is below (Q_before − τ) / δ_max. This holds however severe the drop is within each affected locale. It assumes traffic is fixed and the aggregate starts above the alert threshold τ. Masking is a property of using one traffic-weighted average as the only detection signal, not a tuning problem.

---

## 2. Low-Resource Locale Collapse (LRLC), Proposition 2

**Mechanism:** When quality in a locale falls, engagement and human feedback fall with it. The share of model-generated data in that locale's training mix rises, and that lowers quality further. The effect is strongest where human annotation investment is already weakest.

**Why it matters:** This produces a self-reinforcing cycle. Quality issues in these locales are not just persistent but compounding, and similar starting gaps can end up at very different quality levels depending on how much of the data is model-generated.

**Formal characterization:** Proposition 2 models this as a recursion. Locales with a larger model-generated share α settle at a lower quality than locales with a smaller share, even when both start from similar quality. The fixed point is q* = q_human − [α/(1−α)]ε, clipped to [0, 1].

---

## 3. Aspirational Deferral Lock (ADL), Proposition 3

**Mechanism:** Engineering and product teams allocate attention with a prioritization rule, often implicitly weighting locales or issues by traffic or visible impact. If a locale carries zero weight in that objective, a greedy scheduler never selects its fixes, however real and severe they are, as long as positive-weight work keeps arriving.

**Why it matters:** This is not a failure of judgment or discipline. It is what happens by default whenever attention is allocated by a rule that gives a category zero weight, regardless of how much cumulative harm sits in that category.

**Formal characterization:** Proposition 3 shows that under greedy allocation, a backlog item with zero weight has zero probability of ever being fixed while positive-weight work keeps arriving. A nonzero weight is necessary for selection. Better reporting does not by itself make an organization set that weight above zero.

---

## Relationship Between the Three Patterns

AME explains why the problem stays *invisible* to standard monitoring. LRLC explains why the problem *compounds* rather than staying static once it exists. ADL explains why, even when visible, the problem stays *unaddressed* by standard prioritization. Together they describe a lifecycle: a degradation emerges, is masked from detection, feeds on itself, and fails to get prioritized even if noticed, in the locales least equipped to absorb it.

## Note on Scope

Propositions 1 to 3 are proven under stated assumptions (how aggregate metrics are computed, how model-generated data share affects quality, how greedy allocation behaves). A fourth, toy result covers a special case of the RLSD bound, and the general RLSD bound is a conjecture. Section 6 of the paper is an empirical illustration on public data, with synthetic traffic weights. None of this is a claim about any company's internal systems. See the paper's Limitations section for a full discussion of scope.
