"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

import argparse
from recommender import load_songs, recommend_songs

PRESET_PROFILES = {
    "conflicting_energy_vs_mood": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": True,
    },
    "genre_match_opposite_acoustic": {
        "genre": "jazz",
        "mood": "happy",
        "energy": 0.2,
        "likes_acoustic": False,
    },
    "mood_genre_mismatch_acoustic_bias": {
        "genre": "metal",
        "mood": "calm",
        "energy": 0.1,
        "likes_acoustic": True,
    },
    "extreme_energy_preference": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.0,
        "likes_acoustic": True,
    },
    "ambiguous_neutral_profile": {
        "genre": "electronic",
        "mood": "neutral",
        "energy": 0.5,
        "likes_acoustic": False,
    },
    "AD1": {
        "name": "Conflicting Energy vs Mood",
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": True,
    },
    "AD2": {
        "name": "Electronic but Slow and Sad",
        "genre": "electronic",
        "mood": "sad",
        "energy": 0.1,
        "likes_acoustic": False,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the music recommender with either a preset profile or custom preferences."
    )
    parser.add_argument(
        "--profile",
        choices=PRESET_PROFILES.keys(),
        help="Run one of the built-in test profiles.",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List all built-in preset profiles and exit.",
    )
    parser.add_argument("--genre", help="Favorite genre for a custom profile.")
    parser.add_argument("--mood", help="Favorite mood for a custom profile.")
    parser.add_argument("--energy", type=float, help="Target energy for a custom profile.")
    acoustic_group = parser.add_mutually_exclusive_group()
    acoustic_group.add_argument(
        "--likes-acoustic",
        dest="likes_acoustic",
        action="store_true",
        help="Prefer acoustic songs for a custom profile.",
    )
    acoustic_group.add_argument(
        "--no-likes-acoustic",
        dest="likes_acoustic",
        action="store_false",
        help="Prefer non-acoustic songs for a custom profile.",
    )
    parser.set_defaults(likes_acoustic=None)
    parser.add_argument("-k", type=int, default=5, help="Number of recommendations to show.")
    return parser.parse_args()


def build_user_prefs(args: argparse.Namespace) -> dict:
    # Use AD1 as default if no profile or custom preferences provided
    if args.profile:
        return PRESET_PROFILES[args.profile].copy()
    
    # Check if any custom preference was provided
    has_custom_prefs = any([args.genre, args.mood, args.energy is not None, args.likes_acoustic is not None])
    
    if not has_custom_prefs:
        return PRESET_PROFILES["AD1"].copy()

    missing = []
    if args.genre is None:
        missing.append("--genre")
    if args.mood is None:
        missing.append("--mood")
    if args.energy is None:
        missing.append("--energy")
    if args.likes_acoustic is None:
        missing.append("--likes-acoustic/--no-likes-acoustic")

    if missing:
        raise ValueError(
            "When not using --profile, you must provide: " + ", ".join(missing)
        )

    return {
        "genre": args.genre,
        "mood": args.mood,
        "energy": args.energy,
        "likes_acoustic": args.likes_acoustic,
    }


def main() -> None:
    args = parse_args()
    if args.list_profiles:
        print("Available preset profiles:")
        for profile_name in PRESET_PROFILES:
            print(f"- {profile_name}")
        return

    songs = load_songs("data/songs.csv")
    
    # If no profile specified, show both AD1 and AD2
    if not args.profile and not any([args.genre, args.mood, args.energy is not None, args.likes_acoustic is not None]):
        for profile_key in ["AD1", "AD2"]:
            user_prefs = PRESET_PROFILES[profile_key].copy()
            recommendations = recommend_songs(user_prefs, songs, k=args.k)
            
            print("\n" + "="*60)
            print("Top recommendations:\n")
            profile_name = user_prefs.get("name", profile_key)
            print(f"Profile: {profile_name}")
            print(f"Preferences: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}\n")
            for song, score, explanation in recommendations:
                print(f"{song['title']} - Score: {score:.2f}")
                print(f"Because: {explanation}")
                print()
        print("="*60)
        return
    
    try:
        user_prefs = build_user_prefs(args)
    except ValueError as error:
        raise SystemExit(error)

    recommendations = recommend_songs(user_prefs, songs, k=args.k)

    print("\nTop recommendations:\n")
    profile_name = user_prefs.get("name", args.profile or "Custom Profile")
    print(f"Profile: {profile_name}")
    print(f"Preferences: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}\n")
    for song, score, explanation in recommendations:
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()