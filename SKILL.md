---
name: leboncoin-product-selection
description: Ranks and selects the best LeBonCoin listings from a provided French JSON export using a natural-language brief, seller signals, and online market-price benchmarking; outputs titles+URLs with clear reasons.
---

# LeBonCoin Product Selection

Pick the best listings **only from the provided JSON** (exported from your script). Convert the user’s brief into filters + a simple scoring rubric, **benchmark prices online**, then return a shortlist with explanations.

## When to use this skill
- You already have a JSON file of LeBonCoin results and want the best options.
- The user asks for “meilleur rapport qualité/prix”, “le moins cher”, “le meilleur”, “neuf”, “avec facture”, etc.
- You must compare listing prices to **current online prices** (new/used) before recommending.

## Inputs

### 1) Brief (natural language)
French or English; **mirror the user’s language** in the final answer.

### 2) Listings JSON (French export from the script)
Top-level array of objects with **only** these fields:
- `title` (str)
- `description` (str)
- `date` (str)
- `price` (float)
- `user_score` (int)
- `nb_user_evaluations` (int)
- `url` (str)

Do not expect (and do not invent): location, shipping, category, brand/model fields, photos, etc.

## Output (simple, explainable)
Return:
1) A short summary of how you interpreted the brief
2) A ranked shortlist (default **Top 3**, unless user asks otherwise)

For each selected listing, it’s sufficient to output:
- **Title**
- **URL**
- A short “Why this one” explanation (2–5 bullets)

## Hard Rules
- Use **only** the listings present in the JSON for selection.
- Do **not** invent missing specs. If a spec is unknown, label it as unknown.
- Do **not** claim “new”, “warranty”, “battery health”, etc. unless it appears in `title`/`description`.
- Online price comparison is **required**. If you cannot access web search, say so and clearly mark recommendations as “without market-price verification”.

---

# Workflow

## Step 1 — Parse the brief into constraints + preferences
Extract:
- **Must-have** constraints (dealbreakers): budget max, “neuf uniquement”, specific model, “facture obligatoire”, etc.
- **Nice-to-have** preferences: brand preference, quiet, lightweight, accessories, etc.
- Decide objective:
  - “rapport qualité/prix”, “meilleure affaire” → **value**
  - “le moins cher” → **lowest price**
  - “le meilleur / premium” → **highest quality (text + trust signals)**

Write your interpretation in 1–2 sentences.

## Step 2 — Extract product identity from each listing (from French text)
From `title` + `description`, try to extract:
- Brand + model (e.g., “Dyson V11”, “Roborock S7”, “iPhone 13 128Go”)
- Variant details that affect price: storage (Go), generation, accessories, condition words

Useful French keywords to detect:
- Condition-ish: `neuf`, `comme neuf`, `jamais utilisé`, `très bon état`, `bon état`, `pour pièces`, `HS`
- Proof: `facture`, `garantie`, `ticket`, `sous garantie`
- Red flags: `urgent`, `à débattre`, `paiement hors site`, `Western Union`, `WhatsApp`

If you can’t reliably identify the model, keep it but mark **“modèle exact non identifié”** and be cautious.

## Step 3 — Online market-price benchmarking (required)
For each serious candidate (and at least the top ~10 by initial fit), estimate **current market price**:

1) Build a query in French using extracted identity:
   - `"Marque Modèle" prix neuf`
   - `"Marque Modèle" prix occasion`
   - Include variant (e.g., `128Go`, `Gen 2`) when relevant.

2) Use at least **2 independent sources** when possible:
   - For new price: large retailers / comparison sites (France/EU).
   - For used price: reputable marketplaces and “sold/completed” style signals when available.

3) Derive a simple benchmark:
   - `market_new_eur` (if relevant)
   - `market_used_range_eur` (low–high) or a typical price

4) Compute a value signal:
   - `delta_vs_used = listing_price - typical_used_price`
   - `discount_vs_new = 1 - listing_price / new_price` (if “neuf” is claimed)

If benchmarking fails (no model or no reliable sources), say: **“prix du marché non vérifiable (modèle/flou)”** and penalize the listing.

## Step 4 — Filter out obvious non-matches
Reject listings that violate must-haves, e.g.:
- Over budget (if strict)
- User asked “neuf” but text suggests used/damaged
- Wrong model/variant if clearly stated
- Strong scam indicators in text (off-platform payment, etc.)

List rejections briefly only if it helps explain why few results remain.

## Step 5 — Score and rank (simple and transparent)
Use a 0–100 score, based on what you actually have:

**A) Fit to brief (0–40)**
- Matches required model/variant
- Mentions required proof (facture/garantie) if asked
- Mentions “neuf” if asked, etc.

**B) Price vs market (0–35)**
- Much better than typical used price → high
- Worse than typical used price → low
- If “neuf”: compare to new price

**C) Seller trust signal (0–15)**
- Higher `user_score` and meaningful `nb_user_evaluations` → higher
- If evaluations are 0, don’t assume bad—just “unknown”

**D) Listing clarity & risk (−10 to +10)**
- Clear, specific description/model/proof → +  
- Vague + no model + red-flag wording → −

> Keep the math lightweight: you can describe the scoring qualitatively, but the ranking must be consistent with the explanations.

## Step 6 — Produce the shortlist (title + URL + why)
Default: **Top 3**.
For each selected listing, include:
- Price (from JSON)
- Your market benchmark (new/used) + sources (briefly named, no long quotes)
- 2–5 bullets: why it’s good, what’s unknown, any risks
- 2–3 recommended questions to ask the seller (only based on the brief)

---

# Example (expected style)

**Interpretation of the need:** best quality/price among these options, prioritizing clear listings and well-rated sellers. I compared model prices online (new/used).

1) **[Titre de l’annonce]**  
URL: https://...  
Why:
- Prix: 120€ ; marché occasion typique: ~150–180€ → bonne affaire
- Modèle clairement identifié dans la description (variante incluse)
- Vendeur: 5/5 avec 42 évaluations → signal de confiance
- Inconnu: facture/garantie non mentionnée → à confirmer

2) **[Titre de l’annonce]**  
URL: https://...  
Why:
- Prix cohérent mais meilleur “pack” (accessoires mentionnés)
- Marché neuf: ~299€ ; annonce “neuf” à 210€ → remise intéressante (si vraiment neuf)
- Risque: “neuf” non prouvé → demander facture + photos scellé

3) **[Titre de l’annonce]**  
URL: https://...  
Why:
- Très bon prix vs marché, mais description courte
- Vendeur peu d’évaluations → prudence, poser questions avant achat
