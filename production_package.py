"""
VYDA AI MOVIE ENGINE
Production Package — Build 019

Creates one structured production package for a scene.

The package combines:

- Scene direction
- Continuity
- Character identities
- Visual references
- Production QC

Future workers can consume this package for:

- Image generation
- Video generation
- Voice generation
- Lip-sync
- Music
- Sound effects

The user creates the world.
VYDA adapts to it.
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


class ProductionPackageBuilder:

    def __init__(
        self,
        movie: MoviePlan,
        director: MovieDirector,
        scene_director: SceneDirector,
        reference_engine: CharacterReferenceEngine,
    ):

        self.movie = movie
        self.director = director
        self.scene_director = scene_director
        self.reference_engine = reference_engine

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

    def build(
        self,
        scene_id: str,
    ) -> Dict[str, Any]:
        """
        Build a complete production package
        for one scene.

        The package is blocked if QC fails.
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

                "qc":
                    qc_report,

                "identity":
                    identity_validation,

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

        return {
            "status":
                "READY",

            "scene_id":
                scene_id,

            "package": {

                "scene":
                    {
                        "scene_id":
                            scene_brief.scene_id,

                        "location_id":
                            scene_brief.location_id,

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

                "character_identities":
                    identity_data,

                "qc":
                    qc_report,
            },
        }

    def validate(
        self,
        scene_id: str,
    ) -> dict:
        """
        Validate whether a complete production
        package can be created.
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
      }
