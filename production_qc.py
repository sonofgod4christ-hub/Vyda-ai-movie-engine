"""
VYDA AI MOVIE ENGINE
Production QC — Build 014

Connects Quality Control to the Movie Director.

Purpose:
- Validate a movie before production.
- Validate individual scenes before generation.
- Prevent known structural errors from moving forward.
- Keep QC separate from creative decisions.

The user creates the world.
VYDA adapts to it.
"""

from typing import Dict, Any

from movie_brain import MoviePlan
from movie_director import MovieDirector
from quality_control import QualityControl


class ProductionQualityControl:

    def __init__(
        self,
        movie: MoviePlan,
        director: MovieDirector,
    ):
        self.movie = movie
        self.director = director
        self.qc = QualityControl()

    def validate_movie(self) -> dict:
        """
        Validate the complete movie structure.
        """

        movie_data = {
            "title": self.movie.title,
            "story_idea": self.movie.logline,

            "characters": [
                {
                    "character_id": character.character_id,
                    "name": character.name,
                }
                for character in self.movie.characters
            ],

            "scenes": [
                {
                    "scene_id": scene.scene_id,
                    "characters": scene.characters,
                }
                for scene in self.movie.scenes
            ],

            "dialogue": [],
        }

        return self.qc.validate_movie(
            movie_data
        )

    def validate_scene(
        self,
        scene_id: str,
    ) -> dict:
        """
        Validate one scene before generation.
        """

        scene = next(
            (
                scene
                for scene in self.movie.scenes
                if scene.scene_id == scene_id
            ),
            None,
        )

        if scene is None:
            return {
                "status": "NEEDS_REVIEW",
                "errors": [
                    f"Scene '{scene_id}' was not found."
                ],
                "warnings": [],
            }

        self.qc.reset()

        character_ids = {
            character.character_id
            for character in self.movie.characters
        }

        if not scene.location_id:
            self.qc.errors.append(
                f"{scene_id}: Missing location."
            )

        for character_id in scene.characters:

            if character_id not in character_ids:
                self.qc.errors.append(
                    f"{scene_id}: Unknown character "
                    f"{character_id}."
                )

        if scene.duration_seconds < 0:
            self.qc.errors.append(
                f"{scene_id}: Invalid duration."
            )

        return {
            "status": (
                "PASS"
                if not self.qc.errors
                else "NEEDS_REVIEW"
            ),

            "scene_id": scene_id,

            "errors": list(
                self.qc.errors
            ),

            "warnings": list(
                self.qc.warnings
            ),
        }

    def can_proceed(
        self,
        scene_id: str,
    ) -> bool:
        """
        Returns True only when the scene passes QC.
        """

        result = self.validate_scene(
            scene_id
        )

        return result["status"] == "PASS"

    def get_qc_report(
        self,
        scene_id: str,
    ) -> dict:
        """
        Return a production-ready QC report.
        """

        movie_result = self.validate_movie()

        if movie_result["status"] != "PASS":
            return {
                "status": "NEEDS_REVIEW",
                "stage": "MOVIE",
                "movie": movie_result,
            }

        scene_result = self.validate_scene(
            scene_id
        )

        return {
            "status": scene_result["status"],
            "stage": "SCENE",
            "movie": movie_result,
            "scene": scene_result,
      }
