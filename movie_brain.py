"""
VYDA AI MOVIE ENGINE
Movie Brain — Build 001

Purpose:
Turn a simple story idea into a structured movie production plan.

This is the foundation of the Movie Brain.
No video generation, image generation, voice generation,
or external AI provider is connected yet.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Character:
    character_id: str
    name: str
    age: str
    role: str
    personality: List[str] = field(default_factory=list)


@dataclass
class Scene:
    scene_id: str
    location: str
    time: str
    characters: List[str]
    action: str
    dialogue: List[str] = field(default_factory=list)


@dataclass
class MoviePlan:
    title: str
    logline: str
    genre: str
    theme: str
    characters: List[Character]
    scenes: List[Scene]


class MovieBrain:
    """
    Core director/brain of VYDA AI Movie Engine.

    Future versions will connect this brain to:
    - AI screenplay generation
    - Character image generation
    - Video generation
    - Voice generation
    - Lip-sync
    - Music
    - Sound effects
    - Movie assembly
    """

    def create_movie_plan(
        self,
        title: str,
        logline: str,
        genre: str,
        theme: str,
        characters: List[Character],
        scenes: List[Scene],
    ) -> MoviePlan:

        return MoviePlan(
            title=title,
            logline=logline,
            genre=genre,
            theme=theme,
            characters=characters,
            scenes=scenes,
        )


if __name__ == "__main__":

    brain = MovieBrain()

    movie = brain.create_movie_plan(
        title="The Second Chance",
        logline="A mother gets one opportunity to repair the relationship with her daughter.",
        genre="Drama",
        theme="Family and forgiveness",
        characters=[
            Character(
                character_id="CHAR-001",
                name="Ejiro",
                age="35",
                role="Mother",
                personality=["strong", "loving", "protective"],
            ),
            Character(
                character_id="CHAR-002",
                name="Tega",
                age="15",
                role="Daughter",
                personality=["quiet", "emotional", "intelligent"],
            ),
        ],
        scenes=[
            Scene(
                scene_id="SCENE-001",
                location="Family Living Room",
                time="Evening",
                characters=["CHAR-001", "CHAR-002"],
                action="Ejiro notices that Tega is unusually quiet.",
                dialogue=[
                    "Ejiro: Tega, my daughter, are you okay?",
                    "Tega: I'm fine, Mummy.",
                ],
            )
        ],
    )

    print("VYDA AI MOVIE ENGINE")
    print("--------------------")
    print(f"Movie: {movie.title}")
    print(f"Genre: {movie.genre}")
    print(f"Theme: {movie.theme}")
    print(f"Characters: {len(movie.characters)}")
    print(f"Scenes: {len(movie.scenes)}")
