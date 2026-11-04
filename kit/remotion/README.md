# Montage Remotion (essai « Culture G espace »)
Composition perso (chiffres animés, anneau, barres, sous-titres mot par mot) écrite avec Remotion (moteur du dépôt calesthio/OpenMontage, AGPL : on ne copie pas son code).
Usage : cloner OpenMontage, `cd remotion-composer && npm install`, copier `culture_index.tsx` dans `src/`, mettre clips/voix/props dans `public/culture/`, puis
`npx remotion render src/culture_index.tsx Culture out.mp4 --browser-executable=<chromium playwright> --gl=angle --concurrency=2 --timeout=180000`.
