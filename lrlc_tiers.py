"""FIDS cross-sectional resource-tier comparison (LRLC proxy), rebuilt from scratch.

Inputs:
  1. NLLB-200 3.3B chrF++ scores (naver/nllb-pruning, scores/FLORES-devtest-202-3B.tsv)
  2. FLORES-200 language names and codes (facebookresearch/flores, flores200/README.md)
  3. Joshi et al. (2020) taxonomy: https://microsoft.github.io/linguisticdiversity/assets/lang2tax.txt  (lines: name,class 0-5)
Usage: python lrlc_tiers.py scores.tsv flores_README.md lang2tax.txt outdir

Rules, fixed before any score was joined:
  - Language name = FLORES name with any "(... script)" removed, lowercased. Script variants of one language share its class.
  - Candidate Joshi names = ALIASES.get(name, [name]). If the candidates give one class, use it. If none match, the language is
    UNMATCHED and excluded. If they give more than one class (the taxonomy lists some languages twice), the language is CONFLICTING and excluded.
  - Tiers: Low = class 0-1, Mid = class 2-3, High = class 4-5.
  - Quality = mean of chrF++ for eng->X and X->eng. Bootstrap: 10,000 resamples, seed 0, percentile 95% interval.
"""
import csv, json, re, sys, os, random, statistics as st
scores, readme, tax, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
rows = list(csv.DictReader(open(scores, encoding="utf-8"), delimiter="\t"))
d = {tuple(r["direction"].split("-")): float(r["chrF++"]) for r in rows}
langs = sorted({x for k in d for x in k} - {"eng_Latn"})
q = {l: (d[("eng_Latn", l)] + d[(l, "eng_Latn")]) / 2 for l in langs}
flores = {}
for line in open(readme, encoding="utf-8"):
    m = re.match(r"\s*(.+?)\s*\|\s*([a-z]{3}_[A-Z][a-z]{3})\s*$", line)
    if m: flores[m.group(2)] = re.sub(r"\s*\(.*?script\)", "", m.group(1)).strip().lower()
flores["sat_Beng"] = flores["sat_Olck"]  # the NLLB scores file labels Santali sat_Beng; FLORES-200 lists it as sat_Olck
joshi = {}
for line in open(tax, encoding="utf-8"):
    line = line.strip()
    if "," in line:
        n, c = line.rsplit(",", 1)
        if c.strip().isdigit(): joshi.setdefault(n.strip().lower(), set()).add(int(c))
ALIASES = {
 "modern standard arabic": ["arabic"], "modern standard arabic (romanized)": ["arabic"], "egyptian arabic": ["egyptian arabic"],
 "standard tibetan": ["tibetan"], "central kurdish": ["kurdish (sorani)"], "northern kurdish": ["kurdish (kurmanji)"],
 "central kanuri": ["kanuri"], "southwestern dinka": ["dinka"], "nigerian fulfulde": ["fulfulde", "fula", "fulani", "ful"],
 "haitian creole": ["haitian creole", "haitian"], "belarusian": ["belarusian", "belorussian"], "waray": ["waray", "waray-waray"],
 "guarani": ["guarani", "guaraní"], "nyanja": ["chichewa"], "rundi": ["kirundi", "rundi"], "kyrgyz": ["kirghiz"],
 "kabiyè": ["kabiye", "kabiyé"], "kikongo": ["kongo"], "ganda": ["luganda"], "plateau malagasy": ["malagasy"],
 "halh mongolian": ["mongolian", "khalkha"], "norwegian nynorsk": ["norwegian (nynorsk)"], "norwegian bokmål": ["norwegian (bokmål)"],
 "central aymara": ["aymara"], "west central oromo": ["oromo"], "eastern panjabi": ["eastern punjabi"], "western persian": ["persian"],
 "southern pashto": ["pashto"], "ayacucho quechua": ["quechua"], "tosk albanian": ["albanian"], "eastern yiddish": ["yiddish"],
 "yue chinese": ["cantonese"], "chinese (simplified)": ["mandarin"], "chinese (traditional)": ["mandarin"], "standard malay": ["malay"], "standard latvian": ["latvian"],
 "northern uzbek": ["uzbek"], "north azerbaijani": ["azerbaijani"], "south azerbaijani": ["southern azerbaijani"],
 "sinhala": ["sinhala", "sinhalese"], "southern sotho": ["sesotho", "sotho"], "meitei": ["meithei"],
 "luxembourgish": ["luxembourgish", "luxemburgeois"], "tamasheq": ["tamashek"], "mossi": ["mooré"], "papiamento": ["papiamentu"],
 "occitan": ["occitan", "provençal"], "acehnese": ["acehnese"], "fon": ["fongbe"],
}
tier = lambda c: "Low" if c <= 1 else ("Mid" if c <= 3 else "High")
data, unmatched, conflicting = [], [], []
for code in langs:
    name = flores[code]; cls = set()
    for cand in ALIASES.get(name, [name]): cls |= joshi.get(cand, set())
    if not cls: unmatched.append(code)
    elif len(cls) > 1: conflicting.append(code)
    else: data.append((code, name, next(iter(cls)), q[code]))
def boot(fn, items, n=10000):
    rnd = random.Random(0); res = []
    for _ in range(n):
        s = [items[rnd.randrange(len(items))] for _ in items]
        try: res.append(fn(s))
        except Exception: pass
    res.sort(); return [round(res[int(0.025 * len(res))], 2), round(res[int(0.975 * len(res)) - 1], 2)]
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def spearman(items):
    a, b = rank([x[2] for x in items]), rank([x[3] for x in items])
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
def gap(items):
    hi = [x[3] for x in items if tier(x[2]) == "High"]; lo = [x[3] for x in items if tier(x[2]) == "Low"]
    return sum(hi) / len(hi) - sum(lo) / len(lo)
res = {"languages_total": len(langs), "matched": len(data), "unmatched": unmatched, "conflicting": conflicting, "tiers": {}, "classes": {}}
for t in ("High", "Mid", "Low"):
    v = [x[3] for x in data if tier(x[2]) == t]
    res["tiers"][t] = {"n": len(v), "mean": round(sum(v) / len(v), 2), "median": round(st.median(v), 2)}
for c in range(6):
    v = [x[3] for x in data if x[2] == c]
    if v: res["classes"][str(c)] = {"n": len(v), "mean": round(sum(v) / len(v), 2)}
res["high_minus_low_gap"] = round(gap(data), 2); res["gap_ci95"] = boot(gap, data)
res["spearman_class_vs_quality"] = round(spearman(data), 3); res["spearman_ci95"] = boot(spearman, data, 3000)
ZH = {"zho_Hans", "zho_Hant", "yue_Hant", "jpn_Jpan"}
sub = [x for x in data if x[0] not in ZH]
res["without_chinese_japanese"] = {"high_mean": round(st.mean(x[3] for x in sub if tier(x[2]) == "High"), 2),
                                   "mid_mean": round(st.mean(x[3] for x in sub if tier(x[2]) == "Mid"), 2), "gap": round(gap(sub), 2)}
json.dump(res, open(os.path.join(out, "lrlc_results.json"), "w"), indent=1)
with open(os.path.join(out, "lrlc_matched_languages.tsv"), "w", encoding="utf-8") as f:
    f.write("code\tname\tjoshi_class\ttier\tchrfpp\n")
    for x in sorted(data, key=lambda x: (-x[2], x[0])): f.write(f"{x[0]}\t{x[1]}\t{x[2]}\t{tier(x[2])}\t{x[3]:.2f}\n")
print(json.dumps(res, indent=1))
