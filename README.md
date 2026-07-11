# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Our music recommendation pipeline transforms qualitative attributes and raw audio measurements into structured, comparative predictions through an explicit, step-by-step mathematical recipe.

### 🛠️ Object Attributes & Feature Map

*   **Song Object Fields:**
    *   `id` (int): Unique primary key database index.
    *   `title` / `artist` (str): Informational string metadata descriptive fields.
    *   `genre` / `mood` (str): Categorical text descriptors used for discrete match evaluations.
    *   `energy` (float): Bounded continuous metric ($0.0$ to $1.0$) representing acoustic intensity.
    *   `tempo_bpm` (float): Rhythmic speed tracking index measured in beats per minute.
    *   `acousticness` (float): Continuous dimension tracking organic vs. synthetic instrumentation properties ($0.0$ to $1.0$).

*   **UserProfile Object Fields:**
    *   `favorite_genre` (str): Anchor style string constraint.
    *   `favorite_mood` (str): Target subjective emotional framework description.
    *   `target_energy` (float): Ideal baseline numerical pacer value.
    *   `likes_acoustic` (bool): Categorical toggle verifying instrumentation preferences.

---

### 🧠 The Finalized Algorithm Recipe

To compute personalized recommendations, our system evaluates individual tracks using a multi-layered scoring matrix before compiling the global output array.

1.  **Categorical Match Filters:**
    *   **Genre Core Weight (`+3.0` points):** Acts as the primary structural boundary anchor to keep tracks closely aligned with a user's explicit style choices.
    *   **Mood Vibe Weight (`+2.0` points):** Provides emotional context flexibility across similar auditory landscapes.
    *   **Acoustic Profile Weight (`+1.0` point):** A binary condition reward if a track matches the user's `likes_acoustic` boolean value.

2.  **Continuous Value Scaling (The Proximity Penalty):**
    To reward tracks whose acoustic signatures sit closest to the user's explicit preference baseline rather than simply favoring high or low boundaries, we enforce an **Absolute Delta Proximity Penalty**:
    $$Penalty = -|Song_{\text{energy}} - User_{\text{target\_energy}}| \times 4.0$$
    The further a song's structural intensity drifts from the user's baseline target, the larger the negative deduction applied to its total evaluation score.

3.  **The Global Ranking Rule:**
    Once every candidate song in the CSV pool has been individually scored, the engine applies its sorting rule: it ranks the entire track array in descending order based on total points and trims the matrix to return the top $k$ choices.

---

### ⚠️ Expected Systemic Biases & Limitations

*   **Taxonomic Filtering Trap:** Because the algorithm uses rigid string checking for genres and moods, it over-prioritizes literal labels. An excellent "chill ambient" track will completely miss the `+3.0` genre bonus if a user's favorite genre is explicitly set to "lofi," artificially deflating high-vibe tracks due to human naming discrepancies.
*   **The Homogeneity Filter Bubble:** The heavy mathematical weights placed on matching existing tags and tight energy deltas mean the system is structurally optimized to reproduce a user's past taste profile. This system will struggle to surprise a user, minimizing discovery or cross-genre experimentation.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Top recommendations:

1. Library Rain - Score: 5.00
Because: genre match (+3.0) | mood match (+2.0) | energy affinity match (-0.00 penalty)

2. Midnight Coding - Score: 4.72
Because: genre match (+3.0) | mood match (+2.0) | energy affinity match (-0.28 penalty)

3. Focus Flow - Score: 2.80
Because: genre match (+3.0) | energy affinity match (-0.20 penalty)

4. Spacewalk Thoughts - Score: 1.72
Because: mood match (+2.0) | energy affinity match (-0.28 penalty)

5. Afro Beats & Chill - Score: 0.80
Because: mood match (+2.0) | energy drift deviation (-1.20 penalty)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



