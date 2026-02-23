---
name: leboncoin-product-selection
description: Select the best LeBonCoin listings from a provided JSON export using the user’s brief + online price benchmarking; return a small ranked shortlist with reasons.
---

# LeBonCoin Product Selection

Select the best items **only from the provided JSON**. Use the user’s brief to filter, **check current market prices online**, then return a ranked shortlist with clear reasons and seller questions.

## Inputs
1) **User brief** (FR/EN). Answer in the same language.
2) **Listings JSON**: array of objects with:
- `title`, `description`, `date`, `price`, `user_score`, `nb_user_evaluations`, `url`

## Output (default)
- 1–2 sentences: how you interpreted the brief
- **Top 3** listings (or fewer if only a few fit)

For each listing:
- **Title** + **URL**
- **Listing price**
- **Market price check** (new and/or used) + 1–2 source names
- **Why it’s a good pick** (2–4 bullets: value, fit, trust, risks/unknowns)
- **Questions for the seller** (2–3)

## Hard rules
- Recommend **only** listings present in the JSON.
- Do **not** invent specs. If unknown, say “unknown”.
- Do not claim “new/warranty/battery health/etc.” unless stated in title/description.
- **Market-price benchmarking is required.** If web access is unavailable, say so and label results “without market-price verification”.
- Avoid high-risk/scam-like listings (off-platform payment, suspicious wording).

## Workflow
1) **Parse the brief**
   - Must-haves (budget max, model, “neuf”, “facture”, etc.)
   - Nice-to-haves

2) **Extract identity from each listing**
   - Brand/model/variant from `title` + `description`
   - Condition/proof keywords (e.g., facture, garantie, comme neuf)
   - Flag unclear model as “exact model unknown”

3) **Benchmark prices online (for serious candidates)**
   - Search “Brand Model price new” and “Brand Model used price”
   - Prefer reputable retailers for new, reputable marketplaces for used
   - Summarize as: typical used range and/or new price

4) **Filter**
   - Remove anything breaking must-haves or showing strong scam signals

5) **Rank (simple logic, no scoring)**
   1. Fit to must-haves
   2. Value vs market price
   3. Trust/risk (seller signals + listing clarity)
   4. Tie-breakers (proof, accessories, clearer description)

Return the shortlist in the required format.