# Pipeline vidéo « Un jour une histoire » (moteur papier découpé)

Public : Malick, TikTok. Style : fond bleu marine, papier crème/orange, sous-titres Anton, sans musique, sons très discrets (impacts + pops, PAS de whoosh de transition), transitions en balayage doux.

## Chaque exécution (1 vidéo)
1. Choisir une histoire vraie NON présente dans `kit/historique.txt` (un titre par ligne), l'ajouter à ce fichier.
2. Écrire `scripts/<slug>.txt` (~45-55 s, ~120-140 mots) : accroche directe et surprenante, faits vérifiés (signaler les incertains), clôture FIXE :
   « Tu connaissais cette histoire ? Dis-le moi en commentaire ! Et si tu as aimé, un like et un abonnement pour la prochaine histoire. »
3. `git pull --rebase`, commit + push (sur main). Le workflow GitHub Actions génère `voix/<slug>.mp3` + `.json` (30-60 s). Attendre (fetch en boucle, max ~6 min).
4. Préparer un dossier de travail : copier `kit/*.py`, `voix/<slug>.{mp3,json}`, `scripts/<slug>.txt`.
   Polices : `npm pack @fontsource/anton @fontsource/archivo-black`, extraire les .woff2 latin 400, convertir en ttf (fontTools + brotli) vers `fonts/Anton.ttf` et `fonts/ArchivoBlack.ttf`.
5. Écrire `scenes_<slug>.py` sur le modèle de `scenes_alcatraz.py` (exports : SCENES, BOUNDS, IMPACTS, POPS ; réutiliser sprites de scenes.py et helpers). Une scène par idée (~2-5 s), bannières au mot prononcé (timestamps dans `voix/<slug>.json`). Illustrations entre y≈300 et 1200 ; bas (~450 px) libre pour l'UI TikTok. Fin = CTA (fonction `cta`).
6. Vérifier : `VID_NAME=<slug> VID_SCENES=scenes_<slug> python3 render.py sheet s.png t1 t2 ...` et regarder les planches (chevauchements, texte hors zone).
7. Rendu : `VID_NAME=<slug> VID_SCENES=scenes_<slug> python3 render.py full` (2 workers), puis
   `VID_SFX=sfx.wav python3 audio.py <slug>.mp3 mix.wav`, puis
   `ffmpeg -y -i <slug>_silent.mp4 -i mix.wav -c:v libx264 -preset slow -crf 21 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest titre_JJMMAAAA.mp4`
8. Livrer DANS LE CHAT : SendUserFile (status proactive, display render) + message avec description TikTok (1 phrase) + ≤4 hashtags + faits incertains. Nom : `titre-court_JJMMAAAA.mp4`.
Ne jamais poser de question : choisir et signaler.
Commits : finir par `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.

## Transitions (retour de Malick : trop de balayages)
- Par défaut AUCUN balayage : les scènes s'enchaînent par simple changement de dessins (les pièces de la nouvelle scène « popent » d'elles-mêmes).
- Balayage de papier uniquement sur 1 à 3 vrais changements de lieu/moment par vidéo : lister leurs instants dans `SWEEPS = [...]` du module de scènes (sinon rien). Pas de son de transition.
