"""
VYDA AI MOVIE ENGINE
Production Controller — Build 015

Coordinates scene preparation before generation.

Production flow:

Movie Director
      ↓
Scene Director
      ↓
Production QC
      ↓
Production Package
      ↓
Future Generation Workers

The controller does not generate media yet.
It prepares and validates the scene first.

The user creates the world.
VYDA adapts to it.
"""

from dataclasses import asdict
from typing import Dict, Any

from movie_brain import MoviePlan
from movie_director import MovieDirector
from scene_director import SceneDirector
from production_qc import ProductionQualityControl


class ProductionController:

    def __init__(
        self,
        movie: MoviePlan,
    ):
        self.movie = movie

        self.director = MovieDirector(
            movie
        )

        self.scene_director = SceneDirector(
            movie,
            self.director
        )

        self.qc = ProductionQualityControl(
            movie,
            self.director
        )

    def prepare_scene(
        self,
        scene_id: str,
    ) -> Dict[str, Any]:
        """
        Prepare a scene for future generation.

        QC must pass before a production package
        can be created.
        """

        qc_report = self.qc.get_qc_report(
            scene_id
        )

        if qc_report["status"] != "PASS":
            return {
                "status": "BLOCKED",
                "scene_id": scene_id,
                "qc": qc_report,
                "production_package": None,
            }

        brief = self.scene_director.prepare_scene(
            scene_id
        )

        return {
            "status": "READY",
            "scene_id": scene_id,
            "qc": qc_report,
            "production_package": {
                "scene": asdict(brief),
            },
        }

    def can_generate(
        self,
        scene_id: str,
    ) -> bool:
        """
        Check whether a scene is allowed
        to move toward generation.
        """

        return self.qc.can_proceed(
            scene_id
        )

    def get_scene_brief(
        self,
        scene_id: str,
    ) -> dict:
        """
        Return the structured scene brief
        without starting generation.
        """

        if not self.can_generate(
            scene_id
        ):
            raise ValueError(
                f"Scene '{scene_id}' "
                "failed production QC."
            )

        brief = self.scene_director.prepare_scene(
            scene_id
        )

        return asdict(brief)
