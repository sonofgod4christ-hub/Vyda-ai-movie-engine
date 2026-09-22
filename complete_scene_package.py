"""
VYDA AI MOVIE ENGINE
Complete Scene Package — Build 034

Compatibility repair.

The Complete Scene Package must use the same
identity systems that belong to the Scene Director.

Production flow:

Movie
    ↓
Movie Director
    ↓
Scene Director
    ↓
Character Identity
    ↓
Dialogue Identity
    ↓
Visual References
    ↓
Continuity
    ↓
QC
    ↓
Complete Scene Package
"""

from typing import Dict, Any

from movie_brain import MoviePlan
from movie_director import MovieDirector
from scene_director import SceneDirector
from production_qc import ProductionQualityControl

from character_reference_engine import (
    CharacterReferenceEngine,
)

from scene_identity_package import (
    SceneIdentityPackage,
)

from scene_dialogue_package import (
    SceneDialoguePackage,
)


class CompleteScenePackage:

    def __init__(
        self,
        movie: MoviePlan,
        director: MovieDirector,
        scene_director: SceneDirector,
        reference_engine: CharacterReferenceEngine = None,
    ):

        self.movie = movie

        self.director = director

        self.scene_director = scene_director

        self.reference_engine = (
            reference_engine
            or CharacterReferenceEngine()
        )

        # IMPORTANT:
        # Use the SAME DialogueEngine that belongs
        # to the SceneDirector.
        self.dialogue_engine = (
            scene_director.dialogue_engine
        )

        self.qc = ProductionQualityControl(
            movie,
            director,
        )

        self._register_visual_identities()

        self.identity_package = (
            SceneIdentityPackage(
                movie=movie,
                scene_director=scene_director,
                reference_engine=(
                    self.reference_engine
                ),
            )
        )

        self.dialogue_package = (
            SceneDialoguePackage(
                movie=movie,
                dialogue_engine=(
                    self.dialogue_engine
                ),
            )
        )

    def _register_visual_identities(
        self,
    ):
        """
        Register every movie character in the
        visual reference engine.

        Actual reference assets can be added
        later without changing this package.
        """

        for character in self.movie.characters:

            if (
                character.character_id
                not in self.reference_engine.characters
            ):

                self.reference_engine.register_character(
                    character_id=(
                        character.character_id
                    ),

                    name=character.name,

                    appearance=(
                        character.appearance
                    ),

                    age=character.age,

                    gender=character.gender,

                    hair=character.hair,

                    eyes=character.eyes,

                    body_type=(
                        character.body_type
                    ),

                    wardrobe_identity=(
                        character.wardrobe
                    ),
                )

    def build(
        self,
        scene_id: str,
    ) -> Dict[str, Any]:
        """
        Build the complete authoritative
        production package for one scene.
        """

        qc_report = self.qc.get_qc_report(
            scene_id
        )

        if qc_report["status"] != "PASS":

            return {
                "status":
                    "BLOCKED",

                "scene_id":
                    scene_id,

                "reason":
                    "Production QC failed.",

                "qc":
                    qc_report,

                "package":
                    None,
            }

        identity_validation = (
            self.identity_package.validate(
                scene_id
            )
        )

        if (
            identity_validation["status"]
            != "PASS"
        ):

            return {
                "status":
                    "BLOCKED",

                "scene_id":
                    scene_id,

                "reason":
                    "Character identity validation failed.",

                "identity":
                    identity_validation,

                "package":
                    None,
            }

        dialogue_validation = (
            self._validate_dialogue_if_present(
                scene_id
            )
        )

        if (
            dialogue_validation["status"]
            != "PASS"
        ):

            return {
                "status":
                    "BLOCKED",

                "scene_id":
                    scene_id,

                "reason":
                    "Dialogue validation failed.",

                "dialogue":
                    dialogue_validation,

                "package":
                    None,
            }

        scene_brief = (
            self.scene_director.prepare_scene(
                scene_id
            )
        )

        identity_data = (
            self.identity_package.build(
                scene_id
            )
        )

        dialogue_data = (
            self._build_dialogue_if_present(
                scene_id
            )
        )

        character_data = (
            self._build_character_data(
                scene_brief
            )
        )

        return {
            "status":
                "READY",

            "scene_id":
                scene_id,

            "package": {

                "scene": {
                    "scene_id":
                        scene_brief.scene_id,

                    "location_id":
                        scene_brief.location_id,

                    "location_name":
                        scene_brief.location_name,

                    "time":
                        scene_brief.time,

                    "characters":
                        scene_brief.characters,

                    "action":
                        scene_brief.action,

                    "dialogue":
                        scene_brief.dialogue,

                    "wardrobe_notes":
                        scene_brief.wardrobe_notes,

                    "emotional_state":
                        scene_brief.emotional_state,

                    "camera":
                        scene_brief.camera,

                    "lighting":
                        scene_brief.lighting,

                    "duration_seconds":
                        scene_brief.duration_seconds,

                    "visual_style":
                        scene_brief.visual_style,

                    "cinematic_style":
                        scene_brief.cinematic_style,

                    "language":
                        scene_brief.language,

                    "dialogue_style":
                        scene_brief.dialogue_style,

                    "continuity":
                        scene_brief.continuity,
                },

                "characters":
                    character_data,

                "character_identities":
                    identity_data,

                "dialogue":
                    dialogue_data,

                "qc":
                    qc_report,
            },
        }

    def validate(
        self,
        scene_id: str,
    ) -> dict:
        """
        Validate the complete scene package.
        """

        result = self.build(
            scene_id
        )

        return {
            "scene_id":
                scene_id,

            "status":
                result["status"],

            "ready_for_generation":
                result["status"] == "READY",

            "reason":
                result.get(
                    "reason",
                    "",
                ),
        }

    def _build_character_data(
        self,
        scene_brief,
    ) -> list:

        characters = []

        for character in (
            scene_brief.character_identities
        ):

            characters.append(
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
            )

        return characters

    def _validate_dialogue_if_present(
        self,
        scene_id: str,
    ):

        if scene_id not in (
            self.dialogue_engine.sequences
        ):

            return {
                "status":
                    "PASS",

                "scene_id":
                    scene_id,

                "message":
                    "No dialogue sequence registered.",
            }

        return self.dialogue_package.validate(
            scene_id
        )

    def _build_dialogue_if_present(
        self,
        scene_id: str,
    ):

        if scene_id not in (
            self.dialogue_engine.sequences
        ):

            return []

        result = (
            self.dialogue_package.build(
                scene_id
            )
        )

        if result["status"] != "READY":

            return []

        return result["dialogue"]
