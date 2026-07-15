"""Command line runner showcasing dynamic recommendation strategies and wrapped table views."""

from typing import Any, Dict, List
from .recommender import load_songs, recommend_songs

def wrap_text(text: str, width: int) -> List[str]:
    """Wraps a string of piped reasons into multiple chunks based on target width."""
    # Split by our divider so we don't break key-value pairs mid-word if possible
    parts = text.split(" | ")
    lines: List[str] = []
    current_line = ""
    
    for part in parts:
        # Re-add pipe separator if we are appending to an active line
        candidate = f"{current_line} | {part}" if current_line else part
        if len(candidate) <= width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = part
            
    if current_line:
        lines.append(current_line)
    return lines

def main() -> None:
    csv_path = "data/songs.csv"
    songs = load_songs(csv_path) 
    print(f"=== [SYSTEM] Initializing Multi-Strategy System Test. Catalog Size: {len(songs)} tracks. ===\n")

    # Populating 5+ advanced continuous preferences
    user_prefs: Dict[str, Any] = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.95,
        "likes_acoustic": False,
        "valence": 0.80,       # High positivity preference
        "danceability": 0.85,  # High groove preference
        "tempo": 125.0         # Club-ready tempo pacing
    }

    strategies = ["balanced", "acoustic", "strict_genre"]
    
    # Define strict column widths for alignment
    col_rank = 6
    col_title = 22
    col_artist = 18
    col_score = 7
    col_explain_width = 65  # Limit audit trail column width so it fits cleanly
    
    total_width = col_rank + col_title + col_artist + col_score + col_explain_width + 12 # plus spacer margins

    for strategy in strategies:
        print("=" * total_width)
        print(f"🚀 VIBEPULSE ENGINE STRATEGY: {strategy.upper()}")
        print(f"   Listening Target: Genre={user_prefs['genre']} | Mood={user_prefs['mood']} | Target Energy={user_prefs['energy']}")
        print(f"   Advanced Targets: Valence={user_prefs['valence']} | Danceability={user_prefs['danceability']} | Tempo={user_prefs['tempo']} BPM")
        print("=" * total_width)

        recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)

        # Print Table Headers
        header = (
            f"{'Rank'.ljust(col_rank)} | "
            f"{'Song Title'.ljust(col_title)} | "
            f"{'Artist'.ljust(col_artist)} | "
            f"{'Score'.ljust(col_score)} | "
            f"{'Algorithmic Explanation / Audit Trail'}"
        )
        print(header)
        print("-" * total_width)

       # Print Rows
        for index, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            title_txt = song['title'][:col_title-2] + ".." if len(song['title']) > col_title else song['title']
            artist_txt = song['artist'][:col_artist-2] + ".." if len(song['artist']) > col_artist else song['artist']
            
            # Wrap the long audit text
            wrapped_reasons = wrap_text(explanation, col_explain_width)
            
            # Combine the index and dot into a single clean string of length col_rank
            rank_str = f"{index}."
            
            # First line contains all the main metadata
            first_explain = wrapped_reasons[0] if wrapped_reasons else ""
            row_line = (
                f"{rank_str.ljust(col_rank)} | "
                f"{title_txt.ljust(col_title)} | "
                f"{artist_txt.ljust(col_artist)} | "
                f"{f'{score:.2f}'.ljust(col_score)} | "
                f"{first_explain}"
            )
            print(row_line)
            
            # If there are wrapped overflow lines, print them perfectly aligned in sub-rows!
            for extra_line in wrapped_reasons[1:]:
                spacer_row = (
                    f"{''.ljust(col_rank)} | "
                    f"{''.ljust(col_title)} | "
                    f"{''.ljust(col_artist)} | "
                    f"{''.ljust(col_score)} | "
                    f"{extra_line}"
                )
                print(spacer_row)
                
            print("-" * total_width)
        print("\n" * 2)

if __name__ == "__main__":
    main()