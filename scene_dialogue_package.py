"""
VYDA AI MOVIE ENGINE
Scene Dialogue Package — Build 020

Connects the Dialogue Engine to scene production.

Purpose:
- Keep every line connected to its speaker.
- Preserve dialogue order.
- Preserve character voice identity.
- Preserve language and accent.
- Preserve emotion and delivery.
- Prepare structured dialogue for future
  voice and lip-sync workers.

The user creates the world.
VYDA adapts to it.
"""

from typing import Dict, Any

from movie_brain import MoviePlan

from dialogue_engine import (
    DialogueEngine,
)

from dialogue_flow import (
    DialogueFlowAnalyzer,
)


class SceneDialoguePackage:

    def __init__(
        self,
        movie: MoviePlan,
        dialogue_engine: DialogueEngine,
    ):

        self.movie = movie

        self.dialogue_engine = (
            dialogue_engine
        )

        self.analyzer = (
            DialogueFlowAnalyzer(
                dialogue_engine
            )
        )

    def build(
        self,
        scene_id: str,
    ) -> Dict[str, Any]:
        """
        Build a structured dialogue package
        for one scene.
        """

        self._find_scene(
            scene_id
        )

        analysis = self.analyzer.analyze(
            scene_id
        )

        if analysis["status"] != "PASS":

            return {
                "status":
                    "BLOCKED",

                "scene_id":
                    scene_id,

                "analysis":
                    analysis,

                "dialogue":
                    None,
            }

        ordered_dialogue = (
            self.analyzer.get_ordered_dialogue(
                scene_id
            )
        )

        return {
            "status":
                "READY",

            "scene_id":
                scene_id,

            "analysis":
                analysis,

            "dialogue":
                ordered_dialogue,
        }

    def validate(
        self,
        scene_id: str,
    ) -> dict:
        """
        Validate dialogue before generation.
        """

        self._find_scene(
            scene_id
        )

        analysis = self.analyzer.analyze(
            scene_id
        )

        return {
            "scene_id":
                scene_id,

            "status":
                analysis["status"],

            "ready_for_voice":
                analysis["status"] == "PASS",

            "errors":
                analysis["errors"],

            "warnings":
                analysis["warnings"],
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
