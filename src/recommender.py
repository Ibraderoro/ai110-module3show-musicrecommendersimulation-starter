import csv
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Song':
        """Helper method to convert a standard data dict into a formal Song object."""
        return cls(
            id=int(d["id"]),
            title=d["title"],
            artist=d["artist"],
            genre=d["genre"],
            mood=d["mood"],
            energy=float(d["energy"]),
            tempo_bpm=float(d["tempo_bpm"]),
            valence=float(d["valence"]),
            danceability=float(d["danceability"]),
            acousticness=float(d["acousticness"])
        )

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Calculates scores using OOP constructs, ranks, and filters top items."""
        user_prefs: Dict[str, Any] = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy
        }
        
        # Explicitly typing the list forces Pylance to understand the tuple indices
        scored_songs: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = score_song(user_prefs, song.__dict__)
            scored_songs.append((song, score))
            
        # Pylance now explicitly tracks x[1] as a float primitive, clearing the warning
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Outputs an audit string detailing why a track matched a profile setup."""
        user_prefs: Dict[str, Any] = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy
        }
        _, reasons = score_song(user_prefs, song.__dict__)
        return f"Recommended because: {', '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """Loads songs from a CSV file, converting numeric strings into standard primitives."""
    songs_pool: List[Dict[str, Any]] = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Explicitly type the local song entry to help static checkers
                song_entry: Dict[str, Any] = {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"].strip().lower(),
                    "mood": row["mood"].strip().lower(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"])
                }
                songs_pool.append(song_entry)
    except Exception as e:
        print(f"Error parsing local CSV dataset path {csv_path}: {e}")
    return songs_pool

def score_song(
    user_prefs: Dict[str, Any], 
    song: Dict[str, Any], 
    strategy: str = "balanced"
) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences dynamically based on selected strategy.
    Strategies available: "balanced", "acoustic", "strict_genre"
    """
    score = 0.0
    reasons: List[str] = []

    # 1. Categorical Genre Match (Variable Weight based on strategy)
    genre_match = song["genre"] == user_prefs["genre"].strip().lower()
    if genre_match:
        # Strict genre mode values genre highly, while acoustic mode shifts weight away
        weight = 5.0 if strategy == "strict_genre" else (1.5 if strategy == "acoustic" else 3.0)
        score += weight
        reasons.append(f"genre match (+{weight:.1f})")
    elif strategy == "strict_genre":
        # Strict genre mode aggressively filters non-matching styles out
        score -= 50.0
        reasons.append("genre mismatch lockout (-50.0)")

    # 2. Categorical Mood Match
    if song["mood"] == user_prefs["mood"].strip().lower():
        weight = 1.0 if strategy == "acoustic" else 2.0
        score += weight
        reasons.append(f"mood match (+{weight:.1f})")

    # 3. Continuous Energy Proximity Penalty
    energy_delta = abs(song["energy"] - user_prefs["energy"])
    energy_penalty = energy_delta * 4.0
    score -= energy_penalty
    if energy_delta <= 0.15:
        reasons.append(f"energy affinity match (-{energy_penalty:.2f} penalty)")
    else:
        reasons.append(f"energy drift deviation (-{energy_penalty:.2f} penalty)")

    # 4. Strategy-Specific Features
    if strategy == "acoustic":
        # Strategy exclusive: Evaluate matches on the organic acousticness primitive
        user_likes_acoustic = user_prefs.get("likes_acoustic", False)
        # Match condition: user likes acoustic and song acousticness >= 0.5, or vice-versa
        song_is_acoustic = song.get("acousticness", 0.0) >= 0.5
        if user_likes_acoustic == song_is_acoustic:
            score += 3.0
            reasons.append("acoustic texture match (+3.0)")
        else:
            score -= 1.5
            reasons.append("acoustic mismatch penalty (-1.5)")

    return round(score, 2), reasons

def recommend_songs(
    user_prefs: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
    strategy: str = "balanced"
) -> List[Tuple[Dict[str, Any], float, str]]:
    """Functional implementation of recommendation logic with active strategy and fairness loops."""
    # 1. Calculate base scoring with chosen strategy
    raw_scored_pool: List[Tuple[Dict[str, Any], float, List[str]]] = []
    for song_dict in songs:
        score, reasons = score_song(user_prefs, song_dict, strategy=strategy)
        raw_scored_pool.append((song_dict, score, list(reasons)))

    # Sort primarily by baseline score 
    raw_scored_pool.sort(key=lambda x: x[1], reverse=True)

    final_recommendations: List[Tuple[Dict[str, Any], float, str]] = []
    seen_artists: Dict[str, int] = {}

    # 2. Apply Dynamic Artist Diversity Penalty
    for song_dict, baseline_score, reasons in raw_scored_pool:
        artist = song_dict["artist"].strip().lower()
        
        if artist in seen_artists:
            seen_artists[artist] += 1
            fairness_penalty = 1.50 * (seen_artists[artist] - 1)
            adjusted_score = round(baseline_score - fairness_penalty, 2)
            reasons.append(f"artist saturation penalty (-{fairness_penalty:.2f})")
        else:
            seen_artists[artist] = 1
            adjusted_score = baseline_score

        explanation = " | ".join(reasons) if reasons else "baseline catalog"
        final_recommendations.append((song_dict, adjusted_score, explanation))

    # 3. Final structural sort
    sorted_recommendations: List[Tuple[Dict[str, Any], float, str]] = sorted(
        final_recommendations,
        key=lambda x: x[1],
        reverse=True,
    )
    return sorted_recommendations[:k]