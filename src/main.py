"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    csv_path = "data/songs.csv"
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.35
}
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        # Combines the index number prefix and the song title text on a single line
        print(f"{index}. {song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()
if __name__ == "__main__":
    main()
