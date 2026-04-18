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

    def _score_song(self, song: Song, user: UserProfile) -> float:
        """
        Calculate a score for a song based on user preferences.
        Higher scores indicate better matches.
        
        Weighting strategy:
        - Genre match: 2.0 (broad category alignment - highest weight): genre is a strong indicator of taste, so it gets the highest weight.
        - Mood match: 1.0 (more personal/emotional alignment)
        - Energy similarity: 1.0 (continuous 0-1 scale)
        - Acoustic preference: 1.0 (continuous 0-1 scale)
        """
        score = 0.0
        
        # Genre match (exact match = 2.0, no match = 0) - highest weight as genre is fundamental
        if song.genre == user.favorite_genre:
            score += 2.0
        
        # Mood match (exact match = 1.0, no match = 0)
        if song.mood == user.favorite_mood:
            score += 1.0
        
        # Energy similarity (1 - absolute difference, since energy is 0-1)
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        score += energy_score
        
        # Acoustic preference
        if user.likes_acoustic:
            score += song.acousticness  # Higher acousticness = higher score
        else:
            score += (1.0 - song.acousticness)  # Lower acousticness = higher score
        
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Score all songs and sort by score descending
        scored_songs = [(song, self._score_song(song, user)) for song in self.songs]
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k songs
        return [song for song, score in scored_songs[:k]]

    def recommend_with_scores(self, user: UserProfile, k: int = 5) -> List[Tuple[Song, float, str]]:
        """
        Return recommendations with scores and explanations.
        """
        scored_songs = [(song, self._score_song(song, user), self.explain_recommendation(user, song)) 
                       for song in self.songs]
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explain why a song was recommended for the user.
        """
        reasons = []
        
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre '{user.favorite_genre}'")
        
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood '{user.favorite_mood}'")
        
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append(f"has energy level close to your target ({song.energy:.2f} vs {user.target_energy:.2f})")
        elif song.energy > user.target_energy:
            reasons.append(f"is more energetic than your usual preference")
        else:
            reasons.append(f"is less energetic than your usual preference")
        
        if user.likes_acoustic:
            if song.acousticness > 0.5:
                reasons.append("has high acoustic elements which you prefer")
            else:
                reasons.append("has some acoustic elements")
        else:
            if song.acousticness < 0.3:
                reasons.append("has low acoustic elements which you prefer")
            else:
                reasons.append("has moderate acoustic elements")
        
        if reasons:
            return f"This song was recommended because it {', '.join(reasons)}."
        else:
            return "This song was recommended based on overall similarity to your preferences."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numerical fields
            song_dict = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song_dict)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Convert dicts to Song objects
    song_objects = []
    for s in songs:
        song = Song(
            id=s['id'],
            title=s['title'],
            artist=s['artist'],
            genre=s['genre'],
            mood=s['mood'],
            energy=s['energy'],
            tempo_bpm=s['tempo_bpm'],
            valence=s['valence'],
            danceability=s['danceability'],
            acousticness=s['acousticness']
        )
        song_objects.append(song)
    
    # Create UserProfile
    user = UserProfile(
        favorite_genre=user_prefs['genre'],
        favorite_mood=user_prefs['mood'],
        target_energy=user_prefs['energy'],
        likes_acoustic=user_prefs.get('likes_acoustic', False)
    )
    
    # Create recommender and get recommendations with scores
    recommender = Recommender(song_objects)
    recommendations = recommender.recommend_with_scores(user, k)
    
    # Convert back to dict format
    result = []
    for song, score, explanation in recommendations:
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }
        result.append((song_dict, score, explanation))
    
    return result
