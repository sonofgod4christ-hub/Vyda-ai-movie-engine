"""
VYDA AI MOVIE ENGINE
Movie Brain — Build 028

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

    personality: List[str] = field(
        default_factory=list
    )

    # Character-specific language identity
    language: str = ""

    # Character-specific voice identity
    voice: str = ""
    accent: str = ""

    relationships: List[str] = field(
        default_factory=list
    )

    notes: str = ""


@dataclass
class Location:
    location_id: str
    name: str

    description: str = ""

    country_or_world: str = ""

    era: str = ""

    visual_style: str = ""

    notes: str = ""


@dataclass
class Scene:
    scene_id: str
    location_id: str

    time: str = ""

    characters: List[str] = field(
        default_factory=list
    )

    wardrobe_notes: str = ""

    emotional_state: str = ""

    action: str = ""

    dialogue: List[str] = field(
        default_factory=list
    )

    camera: str = ""

    lighting: str = ""

    duration_seconds: int = 0

    previous_scene_id: str = ""

    next_scene_id: str = ""

    continuity_notes: str = ""


@dataclass
class MoviePlan:
    title: str
    logline: str
    theme: str

    creative_style: CreativeStyle

    characters: List[Character] = field(
        default_factory=list
    )

    locations: List[Location] = field(
        default_factory=list
    )

    scenes: List[Scene] = field(
        default_factory=list
    )


class MovieBrain:

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
