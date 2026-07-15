"""Command line runner showcasing dynamic recommendation strategies."""

from typing import Any, Dict
from .recommender import load_songs, recommend_songs

def main() -> None:
    csv_path = "data/songs.csv"
    songs = load_songs(csv_path) 
    print(f"=== [SYSTEM] Initializing Multi-Strategy System Test. Catalog Size: {len(songs)} tracks. ===\n")

    # Fixed preference base, adding likes_acoustic parameter
    user_prefs: Dict[str, Any] = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.95,
        "likes_acoustic": False  # User wants purely synthesized/electronic pop elements
    }

    # Dynamic run modes
    strategies = ["balanced", "acoustic", "strict_genre"]

    for strategy in strategies:
        print("=" * 125)
        print(f"🚀 VIBEPULSE ENGINE STRATEGY: {strategy.upper()}")
        print(f"   Listening Target: Genre={user_prefs['genre']} | Mood={user_prefs['mood']} | Target Energy={user_prefs['energy']}")
        print("=" * 125)

        recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)

        # Print Table Headers
        header = f"{'Rank'.ljust(6)} | {'Song Title'.ljust(22)} | {'Artist'.ljust(18)} | {'Score'.ljust(7)} | {'Algorithmic Explanation / Audit Trail'}"
        print(header)
        print("-" * 125)

        # Print Rows
        for index, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            title_txt = song['title'][:20] + ".." if len(song['title']) > 20 else song['title']
            artist_txt = song['artist'][:16] + ".." if len(song['artist']) > 16 else song['artist']
            
            row_line = (
                f"{str(index) + '.'.ljust(5)} | "
                f"{title_txt.ljust(22)} | "
                f"{artist_txt.ljust(18)} | "
                f"{f'{score:.2f}'.ljust(7)} | "
                f"{explanation}"
            )
            print(row_line)
            print("-" * 125)
        print("\n" * 2)

if __name__ == "__main__":
    main()