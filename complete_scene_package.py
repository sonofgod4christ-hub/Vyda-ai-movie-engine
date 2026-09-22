"""
VYDA AI MOVIE ENGINE
Complete Scene Package — Build 034

The authoritative handoff package for one scene.

This package combines:

- Scene direction
- Location
- Characters
- Character identity
- Appearance
- Wardrobe
- Language
- Accent
- Voice
- Dialogue
- Speaker identity
- Emotion
- Continuity
- Character references
- Production QC

Nothing should be sent to a generation worker
until this package is READY.

The package becomes the single source of truth
for future image, video, voice, lip-sync,
music and SFX workers.
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

from dialogue_engine import (
    DialogueEngine,
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
        reference_engine: CharacterReferenceEngine,
        dialogue_engine: DialogueEngine,
    ):

        self.movie = movie

        self.director = director

        self.scene_director = scene_director

        self.reference_engine = (
            reference_engine
        )

        self.dialogue_engine = (
            dialogue_engine
        )

        self.qc = ProductionQualityControl(
            movie,
            director,
        )

        self.identity_package = (
            SceneIdentityPackage(
                movie=movie,
                scene_director=scene_director,
                reference_engine=reference_engine,
            )
        )

        self.dialogue_package = (
            SceneDialoguePackage(
                movie=movie,
                dialogue_engine=dialogue_engine,
            )
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
    ) -> dict:
        """
        Dialogue is optional.

        If a scene has no dialogue sequence,
        the scene remains valid.

        If dialogue exists, every turn must
        pass speaker identity validation.
        """

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

        return result["dialogue"]
