"""Timing des mots (edge-tts WordBoundary) + découpage en blocs de sous-titres."""
import json
import re
import unicodedata

SPOKEN_SYL = {"1976": 8, "1977": 8, "1989": 8, "14": 2}  # années/nombres lus en toutes lettres


def syl(w):
    if w in SPOKEN_SYL:
        return SPOKEN_SYL[w]
    w = unicodedata.normalize("NFC", w.lower())
    g = re.findall(r"[aeiouyàâäéèêëîïôöùûüœ]+", w)
    n = len(g)
    if n > 1 and w.endswith("e") and not w.endswith(("ue", "ée")):
        n -= 1
    return max(1, n)


def tokenize_script(text):
    """Découpe le script en mots avec leur ponctuation finale."""
    toks = []
    for raw in text.replace("«", " ").replace("»", " » ").split():
        core = re.match(r"^[\W_]*([\w'’\-àâäéèêëîïôöùûüçœÀÂÉÈÊÎÔÛÇŒ]+)(.*)$", raw, re.UNICODE)
        if core and core.group(1):
            toks.append([core.group(1), core.group(2)])
        elif toks:
            toks[-1][1] += raw
    return toks


def build_words(json_path, script_text, duration):
    ev = [e for e in json.load(open(json_path, encoding="utf-8")) if e["type"] == "WordBoundary"]
    toks = tokenize_script(script_text)
    words, ti = [], 0
    for e in ev:
        parts = e["text"].split()
        # un évènement peut contenir plusieurs mots (ex. « juillet 1976 ») : on répartit au prorata des syllabes
        total = sum(syl(p) for p in parts)
        t = e["start"]
        for p in parts:
            share = e["dur"] * syl(p) / total
            tok = toks[ti] if ti < len(toks) else [p, ""]
            ti += 1
            words.append({"w": tok[0], "punct": tok[1], "start": t, "end": t + share})
            t += share
    for i, w in enumerate(words):
        w["end"] = min(w["end"], words[i + 1]["start"]) if i + 1 < len(words) else min(w["end"], duration)
    return words


def build_blocks(words, max_words=3, max_chars=15):
    blocks, cur = [], []
    for w in words:
        if cur:
            joined = " ".join(x["w"] for x in cur + [w])
            if len(cur) >= max_words or len(joined) > max_chars or re.search(r"[.!?:,;»…]", cur[-1]["punct"]):
                blocks.append(cur)
                cur = []
        cur.append(w)
    if cur:
        blocks.append(cur)
    # évite les blocs d'un seul mot court quand on peut le rattacher au suivant
    out = []
    for b in blocks:
        out.append(b)
    return out


if __name__ == "__main__":
    import sys
    txt = open("casse_nice_v2.txt", encoding="utf-8").read()
    ws = build_words("casse_nice_v2.json", txt, 52.128)
    print(len(ws), "mots")
    for b in build_blocks(ws):
        print(f"{b[0]['start']:.2f}-{b[-1]['end']:.2f}", " ".join(x["w"] + x["punct"] for x in b))
