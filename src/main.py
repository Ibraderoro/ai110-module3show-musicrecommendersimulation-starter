"""Command line runner for the Music Recommender Simulation Multi-Profile Evaluation."""

from typing import Any, Dict
from .recommender import load_songs, recommend_songs

def main() -> None:
    csv_path = "data/songs.csv"
    songs = load_songs(csv_path) 
    
    print(f"=== [SYSTEM] Initializing Phase 4 Stress Test. Catalog Size: {len(songs)} tracks. ===\n")

    print("🚀 VIBEPULSE RECOMMENDER DISCOVERY DASHBOARD")
    print("~" * 125)
    print()
    
    # Defining 3 distinct evaluation profiles (including an adversarial edge case)
    test_profiles: Dict[str, Dict[str, Any]] = {
        "High-Energy Workout": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.95
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85
        },
        "Adversarial / Conflicting Vibe": {
            "genre": "lofi",
            "mood": "sad",
            "energy": 0.90  # Adversarial conflict: sad mood paired with hyper-intense energy
        }
    }

    for profile_name, prefs in test_profiles.items():
        print("=" * 125)
        print(f"👤 PROFILE EXPERIMENT: {profile_name}")
        print(f"   Criteria: Genre={prefs['genre']} | Mood={prefs['mood']} | Target Energy={prefs['energy']}")
        print("=" * 125)

        recommendations = recommend_songs(prefs, songs, k=3)

        # Table Header Line
        header = f"{'Rank'.ljust(6)} | {'Song Title'.ljust(22)} | {'Artist'.ljust(18)} | {'Score'.ljust(7)} | {'Algorithmic Explanation / Audit Trail'}"
        print(header)
        print("-" * 125)

        # Grid Data Rows
        for index, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            
            # Truncate string overflows cleanly to preserve grid alignment boundaries
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