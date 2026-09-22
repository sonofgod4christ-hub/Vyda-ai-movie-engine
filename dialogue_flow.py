"""
VYDA AI MOVIE ENGINE
Dialogue Flow — Build 012

Analyzes dialogue sequences before generation.

Purpose:
Make conversations structured, ordered, and traceable.

The engine does not assume any particular language,
culture, accent, genre, or storytelling style.
"""

from typing import List

from dialogue_engine import (
    DialogueEngine,
    DialogueTurn,
)


class DialogueFlowAnalyzer:
    """
    Validates and analyzes the flow of a conversation.
    """

    def __init__(
        self,
        dialogue_engine: DialogueEngine,
    ):

        self.dialogue_engine = dialogue_engine

    def analyze(
        self,
        scene_id: str,
    ) -> dict:

        sequence = self.dialogue_engine.get_sequence(
            scene_id
        )

        errors: List[str] = []
        warnings: List[str] = []

        turns = sequence.turns

        if not turns:

            warnings.append(
                "Scene contains no dialogue."
            )

        for index, turn in enumerate(turns):

            # Check speaker identity
            if turn.speaker_id not in (
                self.dialogue_engine.identities
            ):

                errors.append(
                    f"{turn.dialogue_id}: "
                    f"Speaker '{turn.speaker_id}' "
                    "has no registered identity."
                )

            # Check dialogue text
            if not turn.line.strip():

                errors.append(
                    f"{turn.dialogue_id}: "
                    "Dialogue line is empty."
                )

            # Check previous link
            expected_previous = ""

            if index > 0:

                expected_previous = (
                    turns[index - 1].dialogue_id
                )

            if (
                turn.previous_dialogue_id
                != expected_previous
            ):

                errors.append(
                    f"{turn.dialogue_id}: "
                    "Incorrect previous dialogue link."
                )

            # Check next link
            expected_next = ""

            if index < len(turns) - 1:

                expected_next = (
                    turns[index + 1].dialogue_id
                )

            if (
                turn.next_dialogue_id
                != expected_next
            ):

                errors.append(
                    f"{turn.dialogue_id}: "
                    "Incorrect next dialogue link."
                )

            # Check identity consistency
            if turn.speaker_id in (
                self.dialogue_engine.identities
            ):

                identity = (
                    self.dialogue_engine
                    .identities[turn.speaker_id]
                )

                if (
                    turn.language
                    and identity.language
                    and turn.language
                    != identity.language
                ):

                    warnings.append(
                        f"{turn.dialogue_id}: "
                        "Dialogue language differs "
                        "from character language."
                    )

                if (
                    turn.accent
                    and identity.accent
                    and turn.accent
                    != identity.accent
                ):

                    warnings.append(
                        f"{turn.dialogue_id}: "
                        "Dialogue accent differs "
                        "from character accent."
                    )

        return {
            "scene_id": scene_id,

            "status": (
                "PASS"
                if not errors
                else "FAIL"
            ),

            "dialogue_count": len(turns),

            "errors": errors,

            "warnings": warnings,
        }

    def get_ordered_dialogue(
        self,
        scene_id: str,
    ) -> List[dict]:
        """
        Return dialogue in exact speaking order.
        """

        sequence = self.dialogue_engine.get_sequence(
            scene_id
        )

        ordered = []

        for turn in sequence.turns:

            identity = (
                self.dialogue_engine
                .get_character_identity(
                    turn.speaker_id
                )
            )

            ordered.append(
                {
                    "dialogue_id":
                        turn.dialogue_id,

                    "speaker_id":
                        turn.speaker_id,

                    "speaker_name":
                        identity.name,

                    "line":
                        turn.line,

                    "emotion":
                        turn.emotion,

                    "delivery":
                        turn.delivery,

                    "language":
                        turn.language,

                    "accent":
                        turn.accent,

                    "voice_profile":
                        identity.voice_profile,
                }
            )

        return ordered
