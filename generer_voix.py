"""Genere la voix (MP3) pour chaque script .txt du dossier scripts/ qui n'a pas encore de voix.
Lance automatiquement toutes les 5 minutes par launchd (voir installer.sh)."""
import asyncio
import json
from datetime import datetime
from pathlib import Path

import edge_tts

DOSSIER = Path(__file__).resolve().parent
SCRIPTS = DOSSIER / "scripts"
VOIX_DIR = DOSSIER / "voix"

VOIX = "fr-FR-RemyMultilingualNeural"
VITESSE = "+8%"
PITCH = "+0Hz"


def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


async def generer(texte, sortie):
    # ecrit dans un fichier temporaire puis renomme : evite de lire un MP3 incomplet
    # Sauvegarde aussi le timing des mots (.json) pour synchroniser les sous-titres
    tmp = sortie.with_suffix(".tmp")
    events = []
    com = edge_tts.Communicate(texte, VOIX, rate=VITESSE, pitch=PITCH, boundary="WordBoundary")
    with open(tmp, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                events.append({
                    "type": chunk["type"],
                    "start": chunk["offset"] / 1e7,
                    "dur": chunk["duration"] / 1e7,
                    "text": chunk["text"],
                })
    tmp.rename(sortie)
    sortie.with_suffix(".json").write_text(
        json.dumps(events, ensure_ascii=False, indent=1), encoding="utf-8"
    )


async def main():
    SCRIPTS.mkdir(exist_ok=True)
    VOIX_DIR.mkdir(exist_ok=True)
    for txt in sorted(SCRIPTS.glob("*.txt")):
        mp3 = VOIX_DIR / (txt.stem + ".mp3")
        if mp3.exists() and mp3.with_suffix(".json").exists():
            continue
        texte = txt.read_text(encoding="utf-8").strip()
        if not texte:
            continue
        try:
            log(f"Generation : {txt.name}")
            await generer(texte, mp3)
            log(f"OK : {mp3.name}")
        except Exception as e:
            log(f"ECHEC {txt.name} : {e}")


if __name__ == "__main__":
    asyncio.run(main())
