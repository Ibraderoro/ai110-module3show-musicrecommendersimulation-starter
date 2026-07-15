# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

`VibePulse 1.0`

---

## 2. Intended Use  

VibePulse 1.0 is a content-based recommendation engine designed for educational simulation and exploration. It takes user taste inputs (genre, mood, and target intensity) and filters a local music library to predict a ranked list of tracks. It operates under the structural assumption that a user's current music preference can be modeled purely through explicit matching of text categories and distance-based scoring of raw audio features, rather than complex interpersonal listening networks.

---

## 3. How the Model Works  

The model treats recommendation as an analytical sorting problem. When a user requests recommendations, it looks at each song's genre text, subjective mood label, and overall audio energy score (rated on a scale from 0.0 to 1.0). 

* **The Matching Bonus:** If a song's genre exactly matches what the user is looking for, it gets a massive boost (+3.0 points). If the emotional mood matches perfectly, it gets another solid bump (+2.0 points).
* **The Energy Penalty:** For the raw feel of the music, the system calculates how far apart the song's energy is from the user's target energy. The wider this "energy gap," the more points are deducted from the song's total score.
* **The Final Cut:** The system adds up the bonuses and subtracts the gap penalty for every track in the catalog, sorts them from highest to lowest score, and hands the user the top 5 results with a clear breakdown explaining why they won.

---

## 4. Data  

The underlying database consists of a static catalog of **20 tracks** loaded via a flat CSV structure. The collection includes a diverse balance of structural genres (Pop, Rock, Lofi, Synthwave, Electronic, and Acoustic) and emotional moods (Happy, Intense, Chill, and Sad). The dataset was deliberately expanded from the 10-song starter kit to add deep-intensity options like synth riot and lo-fi loops. However, the data represents an extreme simplification of real-world music: it entirely misses critical facets of taste like release years, regional culture, vocal versus instrumental flags, and complex nested sub-genres.

---

## 5. Strengths  

* **Clear Stylistic Separation:** The model works exceptionally well for users with clean, mainstream listening intents (like finding upbeat workout music or high-energy rock anthems).
* **Accurate Vibe Matching:** Because categorical checks carry the heaviest weights, tracks like `Storm Runner` or `Sunrise City` are accurately locked to their appropriate sub-audiences.
* **Balanced Alternative Discovery:** When a track doesn't hit a mood requirement but has a near-perfect acoustic energy fit (such as `Gym Hero` matching the 0.95 energy target with a mere -0.08 penalty), the proximity math successfully elevates it into the top ranking slots as an intuitive alternative option.

---

## 6. Limitations and Bias  

* **Taxonomic Rigidity:** The engine suffers from text-matching bias. Because it checks for exact spelling, a song tagged as "lofi" will get zero genre points from a user looking for "chillhop," completely ignoring their identical tempos and instruments.
* **The Categorical Monopoly:** The `+3.0` and `+2.0` text bonuses drastically overpower the continuous energy math. This means an old or slow lo-fi loop will still be forced onto a high-energy user's feed simply because it shared the literal tag "lofi," regardless of the user's intense activity preference.
* **The Homogeneity Bubble:** The mathematical scoring heavily favors what the user explicitly asks for, making it structurally impossible for the system to introduce healthy random discovery, artistic cross-pollination, or fresh listening paths.

---

## 7. Evaluation  

We ran multi-profile stress tests across three distinct listening personas:

1. **High-Energy Workout:** Successfully pulled up `Sunrise City` and `Gym Hero` by prioritizing high energy metrics.

2. **Deep Intense Rock:** Accurately filtered out pop music in favor of heavy instrumentation, placing `Storm Runner` at the top spot with a score of 4.76.
3. **Adversarial / Conflicting Vibe:** We tested an edge case by pairing a quiet genre (`lofi`) with an aggressive energy target (`0.90`). 

**The Surprise:** The system exposed a major structural loophole during the adversarial test. It ranked `Midnight Coding` first with a positive score of 1.08, completely ignoring that the song's relaxed nature was a mismatch for the requested high-energy environment, simply because the "lofi" text label checked out.

---

## 8. Future Work

* **Fuzzy String Logic:** Replace the rigid text checking with a vector-embedding approach or synonym map so "lofi," "ambient," and "chillout" can share partial matching points.
* **Incorporate Multi-Feature Profiles:** Expand the mathematical profiling to check continuous balances for `danceability`, `acousticness`, and rhythmic speed (`tempo_bpm`).
* **Diversity Penalties:** Introduce a localized filter bubble penalty that docking points from tracks if they share the exact same artist or genre as items already sitting in the top 3 recommendation slots, forcing the algorithm to diversify the user's feed.

---

## 9. Personal Reflection  

This project clearly demonstrated that recommendation algorithms are not magic—they are highly opinionated sets of mathematical design choices. I was fascinated to see how easily a simple point change can create a strict "filter bubble" that shuts out incredible music just because of a rigid text label. It completely changed the way I look at my own commercial music streaming apps; I now recognize that behind every "Daily Mix" is a balancing act of category weights and penalty equations struggling to negotiate the messy, subjective nature of human taste.
