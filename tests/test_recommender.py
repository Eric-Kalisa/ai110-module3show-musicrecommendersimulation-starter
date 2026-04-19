from src.recommender import Song, UserProfile, Recommender, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


"""
def test_edge_case_profiles_return_five_sorted_recommendations():
    profiles = [
        {"genre": "pop", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
        {"genre": "jazz", "mood": "happy", "energy": 0.2, "likes_acoustic": False},
        {"genre": "metal", "mood": "calm", "energy": 0.1, "likes_acoustic": True},
        {"genre": "lofi", "mood": "chill", "energy": 0.0, "likes_acoustic": True},
        {"genre": "electronic", "mood": "neutral", "energy": 0.5, "likes_acoustic": False},
    ]

    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
        Song(
            id=3,
            title="Coffee Shop Stories",
            artist="Slow Stereo",
            genre="jazz",
            mood="relaxed",
            energy=0.3,
            tempo_bpm=70,
            valence=0.7,
            danceability=0.4,
            acousticness=0.8,
        ),
        Song(
            id=4,
            title="Thunder Forge",
            artist="Iron Pulse",
            genre="metal",
            mood="energetic",
            energy=0.9,
            tempo_bpm=140,
            valence=0.5,
            danceability=0.6,
            acousticness=0.1,
        ),
        Song(
            id=5,
            title="Library Rain",
            artist="Paper Lanterns",
            genre="lofi",
            mood="chill",
            energy=0.1,
            tempo_bpm=60,
            valence=0.4,
            danceability=0.3,
            acousticness=0.95,
        ),
    ]

    for user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, [
            {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness,
            }
            for song in songs
        ], k=5)

        assert len(recommendations) == 5
        scores = [score for _, score, _ in recommendations]
        assert scores == sorted(scores, reverse=True)
"""
