# Ketut — Chauffeur Privé à Bali 🚗🌴

Landing page pour réserver **Ketut**, chauffeur privé à Bali, **en direct via WhatsApp**
(+62 818‑0556‑8096) — sans agence, sans commission.

- 🇬🇧 Page anglaise : `index.html` (cible « private driver Bali »)
- 🇫🇷 Page française : `fr/index.html` (cible « chauffeur privé Bali »)
- SEO complet : balises meta, Open Graph, données structurées Schema.org
  (LocalBusiness/TaxiService + FAQPage), `sitemap.xml`, `robots.txt`, hreflang EN/FR.
- Réservation : formulaire qui ouvre WhatsApp avec un message pré-rempli. Aucun backend.

## 🚀 Mettre le site en ligne (GitHub Pages)

1. Fusionner cette branche dans `main` (ouvrir une Pull Request et la merger).
2. Sur GitHub : **Settings → Pages → Build and deployment → Source : GitHub Actions**.
3. Le workflow `.github/workflows/deploy-pages.yml` déploie automatiquement à chaque push sur `main`.
4. Le site sera accessible sur : **https://djomobil.github.io/personal-driver-bali/**

> Alternative sans workflow : Settings → Pages → Source : *Deploy from a branch* → `main` / `/ (root)`.

## 📸 Ajouter la vraie photo de Ketut

WhatsApp n'expose pas publiquement les photos de profil (API privée), le site utilise donc
un avatar de secours. Pour afficher la vraie photo :

1. Enregistrer la photo de Ketut (idéalement carrée, ≥ 600×600 px) sous `assets/ketut.jpg`.
2. Commit + push. C'est tout — les deux pages l'utiliseront automatiquement.

## 📈 Faire remonter le site dans Google (actions essentielles)

Le code est optimisé, mais le référencement rapide dépend surtout de ces actions **hors code** :

1. **Google Search Console** ([search.google.com/search-console](https://search.google.com/search-console)) :
   ajouter la propriété `https://djomobil.github.io/personal-driver-bali/`, soumettre `sitemap.xml`
   et demander l'indexation des 2 pages. C'est le levier n°1 pour apparaître vite.
2. **Fiche Google Business Profile** pour « Ketut Bali Private Driver » (catégorie : service de
   chauffeur) avec le numéro WhatsApp et le lien du site — indispensable pour les recherches locales.
3. **Avis clients** : demander aux clients satisfaits de laisser un avis Google — le facteur de
   classement local le plus puissant.
4. **Nom de domaine personnalisé** (optionnel mais recommandé, ex. `ketutbalidriver.com`) :
   meilleur pour la confiance et le SEO. Configurable dans Settings → Pages → Custom domain
   (penser à mettre à jour les URLs canoniques dans les HTML et `sitemap.xml`).
5. **Liens entrants** : profils TripAdvisor / forums voyage / groupes Facebook Bali qui pointent
   vers le site.

## 🛠️ Structure

```
index.html            # Page principale (EN)
fr/index.html         # Version française
assets/style.css      # Design (vert jungle / sable / or)
assets/site.js        # Formulaire → lien WhatsApp pré-rempli
assets/ketut.jpg      # (à ajouter) vraie photo de Ketut
assets/ketut-avatar.svg # Avatar de secours
assets/og-image.png   # Image de partage (réseaux sociaux)
sitemap.xml, robots.txt, 404.html
```
