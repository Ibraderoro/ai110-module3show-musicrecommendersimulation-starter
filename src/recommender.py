import csv
from typing import List, Dict, Tuple, Optional
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
    def from_dict(cls, d: Dict) -> 'Song':
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
        # Convert the OOP UserProfile into a standard dictionary format for score logic uniformity
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy
        }
        
        scored_songs = []
        for song in self.songs:
            # Safely pass the song object attributes as a dictionary map
            score, _ = score_song(user_prefs, song.__dict__)
            scored_songs.append((song, score))
            
        # Sort in-place by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Outputs an audit string detailing why a track matched a profile setup."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy
        }
        _, reasons = score_song(user_prefs, song.__dict__)
        return f"Recommended because: {', '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file, converting numeric strings into standard primitives."""
    songs_pool = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                songs_pool.append({
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
                })
    except Exception as e:
        print(f"Error parsing local CSV dataset path {csv_path}: {e}")
    return songs_pool

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences. Expected format: (score, reasons)"""
    score = 0.0
    reasons = []

    # 1. Categorical Genre Match evaluation (Weight: +3.0)
    if song["genre"] == user_prefs["genre"].strip().lower():
        score += 3.0
        reasons.append(f"genre match (+3.0)")

    # 2. Categorical Mood Match evaluation (Weight: +2.0)
    if song["mood"] == user_prefs["mood"].strip().lower():
        score += 2.0
        reasons.append(f"mood match (+2.0)")

    # 3. Continuous Absolute Delta Proximity Penalty for Energy Alignment
    energy_delta = abs(song["energy"] - user_prefs["energy"])
    energy_penalty = energy_delta * 4.0
    score -= energy_penalty
    
    if energy_delta <= 0.15:
        reasons.append(f"energy affinity match (-{energy_penalty:.2f} penalty)")
    else:
        reasons.append(f"energy drift deviation (-{energy_penalty:.2f} penalty)")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Functional implementation of the recommendation logic required by src/main.py."""
    processed_recommendations = []
    
    for song_dict in songs:
        score, reasons = score_song(user_prefs, song_dict)
        explanation = " | ".join(reasons) if reasons else "baseline catalog"
        processed_recommendations.append((song_dict, score, explanation))
        
    # Non-destructive sorting paradigm using sorted()
    sorted_recommendations = sorted(processed_recommendations, key=lambda x: x[1], reverse=True)
    return sorted_recommendations[:k]