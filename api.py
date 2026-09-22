"""
VYDA AI MOVIE ENGINE
API — Build 029

Universal filmmaking API.

Flow:

User Story
    ↓
API
    ↓
Story Pipeline
    ↓
Movie Brain
    ↓
Movie Plan

Character identity now includes:

Character
    ↓
Language
    ↓
Accent
    ↓
Voice
"""

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from movie_brain import (
    CreativeStyle,
    Character,
    Location,
    Scene,
)

from story_pipeline import StoryPipeline


app = FastAPI(
    title="VYDA AI Movie Engine",
    description="Universal AI filmmaking engine API.",
    version="0.4.0",
)


class CreativeProfile(BaseModel):

    genre: str = ""
    tone: str = ""
    visual_style: str = ""
    cinematic_style: str = ""
    language: str = ""
    dialogue_style: str = ""
    cultural_style: str = ""
    era: str = ""
    rating: str = ""


class CharacterInput(BaseModel):

    character_id: str = ""

    name: str

    age: str = ""
    gender: str = ""

    background: str = ""

    appearance: str = ""
    hair: str = ""
    eyes: str = ""
    body_type: str = ""

    wardrobe: str = ""

    personality: List[str] = Field(
        default_factory=list
    )

    # Character-specific language
    language: str = ""

    # Character-specific voice identity
    voice: str = ""
    accent: str = ""

    relationships: List[str] = Field(
        default_factory=list
    )

    notes: str = ""


class LocationInput(BaseModel):

    location_id: str = ""

    name: str

    description: str = ""

    country_or_world: str = ""

    era: str = ""

    visual_style: str = ""

    notes: str = ""


class SceneInput(BaseModel):

    scene_id: str

    location_id: str

    time: str = ""

    characters: List[str] = Field(
        default_factory=list
    )

    wardrobe_notes: str = ""

    emotional_state: str = ""

    action: str = ""

    dialogue: List[str] = Field(
        default_factory=list
    )

    camera: str = ""

    lighting: str = ""

    duration_seconds: int = 0

    previous_scene_id: str = ""

    next_scene_id: str = ""

    continuity_notes: str = ""


class StoryRequest(BaseModel):

    story_idea: str

    title: str = ""

    theme: str = ""

    creative_profile: CreativeProfile = Field(
        default_factory=CreativeProfile
    )

    characters: List[CharacterInput] = Field(
        default_factory=list
    )

    locations: List[LocationInput] = Field(
        default_factory=list
    )

    scenes: List[SceneInput] = Field(
        default_factory=list
    )


pipeline = StoryPipeline()


@app.get("/")
def home():

    return {
        "engine":
            "VYDA AI Movie Engine",

        "status":
            "online",

        "version":
            "0.4.0",
    }


@app.get("/health")
def health():

    return {
        "status":
            "healthy",

        "engine":
            "VYDA AI Movie Engine",
    }


@app.post("/story")
def receive_story(
    request: StoryRequest,
):
    """
    Receive a complete universal story
    and convert it into a VYDA MoviePlan.
    """

    creative_style = CreativeStyle(
        genre=request.creative_profile.genre,

        tone=request.creative_profile.tone,

        visual_style=(
            request.creative_profile.visual_style
        ),

        cinematic_style=(
            request.creative_profile.cinematic_style
        ),

        language=(
            request.creative_profile.language
        ),

        dialogue_style=(
            request.creative_profile.dialogue_style
        ),

        cultural_style=(
            request.creative_profile.cultural_style
        ),

        era=request.creative_profile.era,

        rating=request.creative_profile.rating,
    )

    characters = []

    for index, character in enumerate(
        request.characters
    ):

        character_id = (
            character.character_id
            or f"CHAR-{index + 1:03d}"
        )

        characters.append(
            Character(
                character_id=character_id,

                name=character.name,

                age=character.age,

                gender=character.gender,

                background=character.background,

                appearance=character.appearance,

                hair=character.hair,

                eyes=character.eyes,

                body_type=character.body_type,

                wardrobe=character.wardrobe,

                personality=character.personality,

                # Character-specific language
                language=character.language,

                # Character-specific voice
                voice=character.voice,

                accent=character.accent,

                relationships=character.relationships,

                notes=character.notes,
            )
        )

    locations = []

    for index, location in enumerate(
        request.locations
    ):

        location_id = (
            location.location_id
            or f"LOC-{index + 1:03d}"
        )

        locations.append(
            Location(
                location_id=location_id,

                name=location.name,

                description=location.description,

                country_or_world=(
                    location.country_or_world
                ),

                era=location.era,

                visual_style=(
                    location.visual_style
                ),

                notes=location.notes,
            )
        )

    scenes = []

    for scene in request.scenes:

        scenes.append(
            Scene(
                scene_id=scene.scene_id,

                location_id=scene.location_id,

                time=scene.time,

                characters=scene.characters,

                wardrobe_notes=(
                    scene.wardrobe_notes
                ),

                emotional_state=(
                    scene.emotional_state
                ),

                action=scene.action,

                dialogue=scene.dialogue,

                camera=scene.camera,

                lighting=scene.lighting,

                duration_seconds=(
                    scene.duration_seconds
                ),

                previous_scene_id=(
                    scene.previous_scene_id
                ),

                next_scene_id=(
                    scene.next_scene_id
                ),

                continuity_notes=(
                    scene.continuity_notes
                ),
            )
        )

    movie = pipeline.build_movie(
        title=request.title,

        story_idea=request.story_idea,

        theme=request.theme,

        creative_style=creative_style,

        characters=characters,

        locations=locations,

        scenes=scenes,
    )

    return {
        "status":
            "READY",

        "message":
            "Story successfully converted "
            "into a VYDA MoviePlan.",

        "movie": {
            "title":
                movie.title,

            "logline":
                movie.logline,

            "theme":
                movie.theme,
        },

        "creative_profile":
            request.creative_profile.model_dump(),

        "characters": [
            {
                "character_id":
                    character.character_id,

                "name":
                    character.name,

                "language":
                    character.language,

                "accent":
                    character.accent,

                "voice":
                    character.voice,
            }

            for character in movie.characters
        ],

        "character_count":
            len(movie.characters),

        "location_count":
            len(movie.locations),

        "scene_count":
            len(movie.scenes),
    }
