"""
VYDA AI MOVIE ENGINE
API — Build 007

Universal Story Input API.

The filmmaker creates the world.
VYDA receives and processes it.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List


app = FastAPI(
    title="VYDA AI Movie Engine",
    description="Universal AI filmmaking engine API.",
    version="0.2.0",
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
    name: str
    age: str = ""
    gender: str = ""
    background: str = ""
    appearance: str = ""
    hair: str = ""
    eyes: str = ""
    body_type: str = ""
    wardrobe: str = ""
    personality: List[str] = Field(default_factory=list)
    voice: str = ""
    accent: str = ""
    relationships: List[str] = Field(default_factory=list)


class LocationInput(BaseModel):
    name: str
    description: str = ""
    country_or_world: str = ""
    era: str = ""
    visual_style: str = ""


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


@app.get("/")
def home():
    return {
        "engine": "VYDA AI Movie Engine",
        "status": "online",
        "version": "0.2.0",
    }


@app.post("/story")
def receive_story(request: StoryRequest):

    return {
        "received": True,

        "story": {
            "title": request.title,
            "story_idea": request.story_idea,
            "theme": request.theme,
        },

        "creative_profile": request.creative_profile.model_dump(),

        "characters": [
            character.model_dump()
            for character in request.characters
        ],

        "locations": [
            location.model_dump()
            for location in request.locations
        ],

        "message": (
            "Story and creative profile received "
            "by the VYDA Movie Engine."
        ),
    }
