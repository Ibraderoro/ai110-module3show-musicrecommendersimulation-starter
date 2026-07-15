# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Resolve static-analysis Pylance warnings (`UnknownMemberType` and sorting lambda type mismatches), implement an active artist diversity penalty loop to prevent echo chambers, and build a clean, auto-truncating, fully padded ASCII terminal dashboard for user recommendations.

**Prompts used:**

1. *"Pylance is complaining about `UnknownMemberType` on the sorting lambda in my recommendation function. How do we explicitly type this array?"*
2. *"How do I implement a 'Diversity Penalty' rule to penalize a song's score if its artist is already present in the top recommendations list?"*
3. *"Write a custom ASCII terminal formatter in `main.py` using native string padding (`.ljust()`) that displays the rank, song title, artist, score, and step-by-step scoring breakdown without requiring third-party libraries like `tabulate`."*

**What did the agent generate or change?**

*   **`src/recommender.py`**:
    *   Upgraded `recommend_songs` to track `seen_artists: Dict[str, int]` during evaluation.
    *   Added a dynamic compound penalty calculation of `-1.50 * (seen_artists[artist] - 1)` to prevent duplicate artists from taking over the feed.
    *   Added explicit type-hinting signatures (`List[Tuple[Dict[str, Any], float, str]]` and `List[Tuple[Song, float]]`) to clear Pylance editor warnings completely.
*   **`src/main.py`**:
    *   Implemented a sequential multi-profile evaluation runner.
    *   Created an ASCII grid table using python's native `.ljust()` spacing and custom vertical pipelines (`|`), featuring automated string truncation (`song['title'][:20] + ".."`) to maintain column layout alignments under all terminals.

**What did you verify or fix manually?**

*   Verified that `pytest` executed completely error-free and passed 100% of validation specs in `0.01s`.
*   Manually ran `python3 -m src.main` to confirm that whenever `Max Pulse` attempted to take a secondary rank position, the console output correctly printed `artist saturation penalty (-1.50)`, pushing the duplicate down the table automatically.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The **Strategy Pattern** (Parameter-driven algorithmic behaviors).

**How did AI help you brainstorm or implement it?**

We brainstormed how to let users change *how* the recommendation logic functions depending on their context. 
The AI suggested a parameterized strategy model: instead of writing three completely different classes, we unified the layout by passing a `strategy` configuration string (`"balanced"`, `"acoustic"`, or `"strict_genre"`) down into a single `score_song` execution pipeline. This keeps our OOP setup compact, highly maintainable, and completely compatible with the existing pytest harness.

**How does the pattern appear in your final code?**

*   **In `src/recommender.py`**:
    *   `score_song(user_prefs, song, strategy="balanced")`: The algorithm reads the strategy flag to dynamically shift weight coefficients (e.g., changing the Genre match reward from `+3.0` to `+5.0` or `+1.5`).
    *   In `"strict_genre"` mode, it implements an aggressive boundary constraint, instantly applying a `-50.0` mismatch lockout penalty to any track that fails a strict string check.
    *   In `"acoustic"` mode, it looks deeper into the continuous acoustic metrics, giving an explicit $+3.0$ reward if the song’s physical acoustic texture matches the user's preference toggle.
*   **In `src/main.py`**:
    *   The loop runs the exact same user profile across different strategies, showcasing completely different outcomes based on the selected algorithm mode.