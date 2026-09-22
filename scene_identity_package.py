"""
VYDA AI MOVIE ENGINE
Scene Identity Package — Build 018

Purpose:
Attach authoritative character identity and
visual reference information to a scene.

This ensures future image/video generation
workers receive the correct character references
for every character appearing in the scene.

The user creates the world.
VYDA adapts to it.
"""

from typing import Dict, List, Any

from movie_brain import MoviePlan

from character_reference_engine import (
    CharacterReferenceEngine,
)

from scene_director import SceneDirector


class SceneIdentityPackage:

    def __init__(
        self,
        movie: MoviePlan,
        scene_director: SceneDirector,
        reference_engine: CharacterReferenceEngine,
    ):

        self.movie = movie
        self.scene_director = scene_director
        self.reference_engine = reference_engine

    def build(
        self,
        scene_id: str,
    ) -> Dict[str, Any]:
        """
        Build the identity package for one scene.
        """

        scene = self._find_scene(
            scene_id
        )

        character_packages: List[dict] = []

        for character_id in scene.characters:

            try:

                identity = (
                    self.reference_engine
                    .build_generation_context(
                        character_id
                    )
                )

                character_packages.append(
                    identity
                )

            except ValueError:

                character_packages.append(
                    {
                        "character_id":
                            character_id,

                        "status":
                            "REFERENCE_NOT_REGISTERED",

                        "references":
                            [],
                    }
                )

        return {
            "scene_id":
                scene.scene_id,

            "characters":
                character_packages,
        }

    def validate(
        self,
        scene_id: str,
    ) -> dict:
        """
        Check that every character in the scene
        has a registered visual identity.
        """

        scene = self._find_scene(
            scene_id
        )

        errors = []

        for character_id in scene.characters:

            try:

                self.reference_engine.get_identity(
                    character_id
                )

            except ValueError:

                errors.append(
                    f"{scene_id}: Character "
                    f"'{character_id}' has no "
                    "registered visual identity."
                )

        return {
            "status":
                "PASS"
                if not errors
                else "NEEDS_REVIEW",

            "scene_id":
                scene_id,

            "errors":
                errors,
        }

    def _find_scene(
        self,
        scene_id: str,
    ):

        for scene in self.movie.scenes:

            if scene.scene_id == scene_id:
                return scene

        raise ValueError(
            f"Scene '{scene_id}' was not found."
      )
