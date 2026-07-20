# Ketut — Chauffeur Privé à Bali 🚗🌴

Landing page pour réserver **Ketut**, chauffeur privé à Bali (plus de 20 ans d'expérience),
**en direct via WhatsApp** (+62 818‑0556‑8096) — sans agence, sans commission.

## 🌍 5 langues (anglais par défaut)

| Langue | URL | Cible SEO |
|---|---|---|
| 🇬🇧 English (défaut) | `/` | private driver Bali |
| 🇫🇷 Français | `/fr/` | chauffeur privé Bali |
| 🇩🇪 Deutsch | `/de/` | privater Fahrer Bali |
| 🇷🇺 Русский | `/ru/` | личный водитель Бали |
| 🇨🇳 中文 | `/zh/` | 巴厘岛私人司机 |

Ce sont les principaux marchés touristiques de Bali. Chaque langue est une **vraie page
statique** (pas de traduction JavaScript) : c'est la seule approche que Google indexe
parfaitement, avec balises `hreflang` croisées, canonical, Open Graph et données
structurées Schema.org (LocalBusiness/TaxiService + FAQPage) localisées.

## 🛠️ Modifier le contenu (système i18n)

Les pages sont **générées** — ne pas éditer les `index.html` à la main :

1. Modifier les textes dans `tools/i18n/<langue>.json` (ou la structure dans `tools/template.html`).
2. Regénérer : `python3 tools/build.py` (produit les 5 pages + `sitemap.xml`).
3. Commit + push.

Le formulaire de réservation ouvre WhatsApp avec un message pré-rempli dans la langue de la
page (`assets/site.js`). Aucun backend : WhatsApp **est** le système de booking — si un jour
il faut un calendrier ou du paiement en ligne, il suffira de brancher un service externe
(Calendly, Stripe payment links…) sans refonte.

## 🚀 Mise en ligne (GitHub Pages)

1. Sur GitHub : **Settings → Pages → Build and deployment → Source : GitHub Actions**.
2. Le workflow `.github/workflows/deploy-pages.yml` déploie à chaque push sur `main`
   (et sur cette branche de développement, pour valider avant fusion).
3. Site : **https://djomobil.github.io/personal-driver-bali/**

## 📸 Ajouter la vraie photo de Ketut

WhatsApp n'expose pas publiquement les photos de profil (API privée) ; le site utilise un
avatar de secours. Pour afficher la vraie photo : enregistrer une image carrée (≥ 600×600 px)
sous `assets/ketut.jpg`, commit, push. Les 5 pages l'utiliseront automatiquement.

L'image de partage réseaux sociaux (`assets/og-image.png`) est générée depuis
`tools/og-source.html` (capture Chromium 1200×630).

## 📈 Faire remonter le site dans Google — les vrais leviers

1. **Google Search Console** : ajouter `https://djomobil.github.io/personal-driver-bali/`,
   soumettre `sitemap.xml`, demander l'indexation. Levier n°1 pour apparaître vite.
2. **Fiche Google Business Profile** « Ketut Bali Private Driver » (catégorie service de
   chauffeur) avec le numéro WhatsApp et le lien du site — indispensable en recherche locale.
3. **Avis Google** de clients satisfaits — le facteur de classement local le plus puissant.
4. **Nom de domaine personnalisé** (ex. `ketutbalidriver.com`) : Settings → Pages → Custom
   domain, puis mettre à jour `BASE` dans `tools/build.py` et relancer le build.
5. **Liens entrants** : TripAdvisor, forums voyage, groupes Facebook/WeChat/Telegram Bali.

## Structure

```
index.html                  # EN (générée)
fr/ de/ ru/ zh/index.html   # autres langues (générées)
tools/template.html         # structure de page commune
tools/i18n/*.json           # textes par langue
tools/build.py              # générateur (pages + sitemap)
tools/og-source.html        # source de l'image de partage
assets/                     # style.css, site.js, avatar, og-image.png, favicon
sitemap.xml, robots.txt, 404.html
```
