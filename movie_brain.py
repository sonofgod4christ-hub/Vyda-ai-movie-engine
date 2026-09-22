"""
VYDA AI MOVIE ENGINE
Movie Brain — Build 004

Universal Creative Profile + Character Bible

VYDA is not tied to any country, culture, language,
genre, visual style, or character type.

The user creates the world.
VYDA adapts to it.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CreativeStyle:
    """
    Defines the creative world chosen by the filmmaker.
    """

    genre: str
    tone: str = ""
    visual_style: str = ""
    cinematic_style: str = ""
    language: str = ""
    dialogue_style: str = ""
    cultural_style: str = ""
    era: str = ""
    rating: str = ""


@dataclass
class Character:
    """
    Universal character bible.

    Every character is created from user-defined information.
    """

    character_id: str
    name: str
    age: str = ""
    gender: str = ""
    background: str = ""
    appearance: str = ""
    hair: str = ""
    eyes: str = ""
    body_type: str = ""
    wardrobe: str = ""
    personality: List[str] = field(default_factory=list)
    voice: str = ""
    accent: str = ""
    relationships: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Location:
    """
    Universal movie location.
    """

    location_id: str
    name: str
    description: str = ""
    country_or_world: str = ""
    era: str = ""
    visual_style: str = ""
    notes: str = ""


@dataclass
class Scene:
    """
    Scene production and continuity information.
    """

    scene_id: str
    location_id: str
    time: str = ""
    characters: List[str] = field(default_factory=list)

    wardrobe_notes: str = ""
    emotional_state: str = ""
    action: str = ""

    dialogue: List[str] = field(default_factory=list)

    camera: str = ""
    lighting: str = ""
    duration_seconds: int = 0

    previous_scene_id: str = ""
    next_scene_id: str = ""

    continuity_notes: str = ""


@dataclass
class MoviePlan:
    """
    Complete production blueprint for a movie.
    """

    title: str
    logline: str
    theme: str

    creative_style: CreativeStyle

    characters: List[Character] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)


class MovieBrain:
    """
    Core director/brain of VYDA AI Movie Engine.

    Future systems will connect this brain to:

    - AI screenplay generation
    - Character image generation
    - Video generation
    - Voice generation
    - Lip-sync
    - Music
    - Sound effects
    - Continuity engine
    - Quality control
    - Movie assembly
    """

    def create_movie_plan(
        self,
        title: str,
        logline: str,
        theme: str,
        creative_style: CreativeStyle,
        characters: List[Character],
        locations: List[Location],
        scenes: List[Scene],
    ) -> MoviePlan:

        return MoviePlan(
            title=title,
            logline=logline,
            theme=theme,
            creative_style=creative_style,
            characters=characters,
            locations=locations,
            scenes=scenes,
        )
