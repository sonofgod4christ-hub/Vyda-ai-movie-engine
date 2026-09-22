"""
VYDA AI MOVIE ENGINE
Scene Director — Build 032

Connects the Movie Director, scene information,
character identities, dialogue identity, and
continuity into one scene production brief.

The user creates the world.
VYDA directs the scene.
"""

from dataclasses import dataclass, field
from typing import List

from movie_director import MovieDirector
from dialogue_engine import (
    DialogueEngine,
)
from identity_bridge import IdentityBridge


@dataclass
class SceneCharacter:
    character_id: str
    name: str

    language: str = ""
    accent: str = ""
    voice: str = ""

    appearance: str = ""
    wardrobe: str = ""

    emotional_state: str = ""


@dataclass
class SceneProductionBrief:

    scene_id: str

    location_id: str
    location_name: str

    time: str = ""

    characters: List[str] = field(
        default_factory=list
    )

    character_identities: List[
        SceneCharacter
    ] = field(
        default_factory=list
    )

    action: str = ""

    dialogue: List[str] = field(
        default_factory=list
    )

    camera: str = ""

    lighting: str = ""

    wardrobe_notes: str = ""

    emotional_state: str = ""

    duration_seconds: int = 0

    visual_style: str = ""

    cinematic_style: str = ""

    language: str = ""

    dialogue_style: str = ""

    continuity: dict = field(
        default_factory=dict
    )


class SceneDirector:

    def __init__(
        self,
        movie_director: MovieDirector,
    ):

        self.movie_director = movie_director

        self.dialogue_engine = (
            DialogueEngine()
        )

        self.identity_bridge = (
            IdentityBridge(
                self.dialogue_engine
            )
        )

        self._register_movie_characters()

    def _register_movie_characters(
        self,
    ):

        characters = (
            self.movie_director.movie.characters
        )

        self.identity_bridge.register_characters(
            characters
        )

    def _build_character_identities(
        self,
        scene,
    ) -> List[SceneCharacter]:

        identities = []

        for character_id in scene.characters:

            identity = (
                self.identity_bridge.get_identity(
                    character_id
                )
            )

            if identity is None:
                raise ValueError(
                    "Scene references an unknown "
                    f"character: {character_id}"
                )

            identities.append(
                SceneCharacter(
                    character_id=(
                        identity.character_id
                    ),

                    name=identity.name,

                    language=identity.language,

                    accent=identity.accent,

                    voice=identity.voice_profile,

                    appearance=(
                        identity.appearance
                    ),

                    wardrobe=(
                        identity.wardrobe_identity
                    ),

                    emotional_state=(
                        scene.emotional_state
                    ),
                )
            )

        return identities

    def prepare_scene(
        self,
        scene_id: str,
    ) -> SceneProductionBrief:

        context = (
            self.movie_director.prepare_scene(
                scene_id
            )
        )

        scene = context["scene"]

        location = context["location"]

        character_identities = (
            self._build_character_identities(
                scene
            )
        )

        return SceneProductionBrief(

            scene_id=scene.scene_id,

            location_id=scene.location_id,

            location_name=location.name,

            time=scene.time,

            characters=scene.characters,

            character_identities=(
                character_identities
            ),

            action=scene.action,

            dialogue=scene.dialogue,

            camera=scene.camera,

            lighting=scene.lighting,

            wardrobe_notes=(
                scene.wardrobe_notes
            ),

            emotional_state=(
                scene.emotional_state
            ),

            duration_seconds=(
                scene.duration_seconds
            ),

            visual_style=(
                context["creative_style"][
                    "visual_style"
                ]
            ),

            cinematic_style=(
                context["creative_style"][
                    "cinematic_style"
                ]
            ),

            language=(
                context["creative_style"][
                    "language"
                ]
            ),

            dialogue_style=(
                context["creative_style"][
                    "dialogue_style"
                ]
            ),

            continuity=(
                context["continuity"]
            ),
        )

    def get_scene_brief(
        self,
        scene_id: str,
    ) -> dict:

        brief = self.prepare_scene(
            scene_id
        )

        return {
            "scene_id":
                brief.scene_id,

            "location": {
                "location_id":
                    brief.location_id,

                "name":
                    brief.location_name,

                "time":
                    brief.time,
            },

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

                    "appearance":
                        character.appearance,

                    "wardrobe":
                        character.wardrobe,

                    "emotional_state":
                        character.emotional_state,
                }

                for character
                in brief.character_identities
            ],

            "action":
                brief.action,

            "dialogue":
                brief.dialogue,

            "camera":
                brief.camera,

            "lighting":
                brief.lighting,

            "wardrobe_notes":
                brief.wardrobe_notes,

            "emotional_state":
                brief.emotional_state,

            "duration_seconds":
                brief.duration_seconds,

            "visual_style":
                brief.visual_style,

            "cinematic_style":
                brief.cinematic_style,

            "language":
                brief.language,

            "dialogue_style":
                brief.dialogue_style,

            "continuity":
                brief.continuity,
        }
