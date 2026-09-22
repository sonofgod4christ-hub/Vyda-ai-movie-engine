"""
VYDA AI MOVIE ENGINE
Quality Control — Build 013

Production validation layer.

Purpose:
Catch structural and continuity problems before
content moves to generation or final assembly.
"""

from typing import List, Dict, Any


class QualityControl:

    def __init__(self):

        self.errors: List[str] = []
        self.warnings: List[str] = []

    def reset(self):

        self.errors = []
        self.warnings = []

    def check_required_text(
        self,
        value: str,
        field_name: str,
    ):

        if not value or not value.strip():

            self.errors.append(
                f"Missing required field: {field_name}"
            )

    def check_character_ids(
        self,
        characters: List[Dict[str, Any]],
    ):

        seen = set()

        for character in characters:

            character_id = character.get(
                "character_id"
            )

            if not character_id:

                self.errors.append(
                    "Character is missing character_id."
                )

                continue

            if character_id in seen:

                self.errors.append(
                    f"Duplicate character ID: "
                    f"{character_id}"
                )

            seen.add(character_id)

    def check_scene_characters(
        self,
        scenes: List[Dict[str, Any]],
        character_ids: set,
    ):

        for scene in scenes:

            scene_id = scene.get(
                "scene_id",
                "UNKNOWN"
            )

            for character_id in scene.get(
                "characters",
                []
            ):

                if character_id not in character_ids:

                    self.errors.append(
                        f"{scene_id}: "
                        f"Unknown character "
                        f"{character_id}."
                    )

    def check_dialogue(
        self,
        dialogue: List[Dict[str, Any]],
        character_ids: set,
    ):

        for turn in dialogue:

            dialogue_id = turn.get(
                "dialogue_id",
                "UNKNOWN"
            )

            speaker_id = turn.get(
                "speaker_id"
            )

            line = turn.get(
                "line",
                ""
            )

            if speaker_id not in character_ids:

                self.errors.append(
                    f"{dialogue_id}: "
                    f"Unknown speaker "
                    f"{speaker_id}."
                )

            if not line.strip():

                self.errors.append(
                    f"{dialogue_id}: "
                    "Empty dialogue."
                )

    def check_identity(
        self,
        identity: Dict[str, Any],
    ):

        character_id = identity.get(
            "character_id",
            "UNKNOWN"
        )

        name = identity.get(
            "name",
            ""
        )

        self.check_required_text(
            name,
            f"{character_id}.name"
        )

    def validate_movie(
        self,
        movie: Dict[str, Any],
    ) -> dict:
        """
        Run structural checks against a movie.
        """

        self.reset()

        self.check_required_text(
            movie.get("title", ""),
            "movie.title"
        )

        self.check_required_text(
            movie.get("story_idea", ""),
            "movie.story_idea"
        )

        characters = movie.get(
            "characters",
            []
        )

        scenes = movie.get(
            "scenes",
            []
        )

        dialogue = movie.get(
            "dialogue",
            []
        )

        self.check_character_ids(
            characters
        )

        character_ids = {
            character.get("character_id")
            for character in characters
            if character.get("character_id")
        }

        self.check_scene_characters(
            scenes,
            character_ids
        )

        self.check_dialogue(
            dialogue,
            character_ids
        )

        return {
            "status": (
                "PASS"
                if not self.errors
                else "NEEDS_REVIEW"
            ),

            "errors": list(self.errors),

            "warnings": list(self.warnings),
                  }
