"""FIDS empirical illustration, rebuilt from raw scores. One script, no hidden inputs.

Data: NLLB-200 3.3B dense, FLORES-200 devtest, chrF++, 202 x 201 = 40,602 directions,
from github.com/naver/nllb-pruning (scores/FLORES-devtest-202-3B.tsv).
Usage: python fids_empirical.py path/to/FLORES-devtest-202-3B.tsv outdir

Per-language quality q_i = mean(chrF++ eng->i, chrF++ i->eng), 201 non-English languages.
Traffic weights are SYNTHETIC. The primary scheme was fixed before looking at results:
10 major languages share 80% of traffic equally, the other 191 share 20% equally.
Sensitivity schemes are listed in SCHEMES and all are reported.
"""
import csv, json, sys, os
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
rows = list(csv.DictReader(open(src, encoding="utf-8"), delimiter="\t"))
d = {tuple(r["direction"].split("-")): float(r["chrF++"]) for r in rows}
langs = sorted({x for k in d for x in k} - {"eng_Latn"})
assert len(rows) == 40602 and len(langs) == 201
q = {l: (d[("eng_Latn", l)] + d[(l, "eng_Latn")]) / 2 for l in langs}
TOP = ["spa_Latn", "zho_Hans", "por_Latn", "fra_Latn", "deu_Latn", "arb_Arab", "rus_Cyrl", "jpn_Jpan", "hin_Deva", "ind_Latn"]
assert all(t in q for t in TOP)
def weights(top_share, split="equal"):
    rest = [l for l in q if l not in TOP]
    if split == "equal": wt = [1 / len(TOP)] * len(TOP)
    else:
        z = [1 / (i + 1) for i in range(len(TOP))]; wt = [x / sum(z) for x in z]
    w = {l: top_share * wt[i] for i, l in enumerate(TOP)}
    w.update({l: (1 - top_share) / len(rest) for l in rest})
    return w
SCHEMES = {"primary: top10 80% equal, rest 20% equal": (0.8, "equal"),
           "top10 80%, Zipf within top10": (0.8, "zipf"),
           "top10 60% equal": (0.6, "equal"),
           "top10 90% equal": (0.9, "equal")}
order = sorted(q, key=q.get)
worst, bot10 = order[0], order[:10]
res = {"directions": len(rows), "languages": len(q), "unweighted_mean": round(sum(q.values()) / len(q), 2),
       "worst_language": worst, "worst_score": round(q[worst], 2), "bottom10": bot10,
       "bottom10_mean": round(sum(q[l] for l in bot10) / 10, 2), "schemes": {}}
for name, (s, sp) in SCHEMES.items():
    w = weights(s, sp); Q = sum(w[l] * q[l] for l in q)
    w_b = sum(w[l] for l in bot10)
    res["schemes"][name] = {"Q_agg": round(Q, 2), "worst_traffic_share_pct": round(w[worst] * 100, 3),
        "gap_to_worst": round(Q - q[worst], 2), "bottom10_traffic_share_pct": round(w_b * 100, 2),
        "drop_in_Q_agg_if_bottom10_collapse_to_0": round(sum(w[l] * q[l] for l in bot10), 2)}
json.dump(res, open(os.path.join(out, "ame_results.json"), "w"), indent=1)
with open(os.path.join(out, "per_language_chrf.tsv"), "w") as f:
    f.write("language\tchrfpp_mean_of_both_directions\n")
    for l in order: f.write(f"{l}\t{q[l]:.2f}\n")
print(json.dumps(res, indent=1))
