"""
VYDA AI MOVIE ENGINE
Dialogue Engine — Build 030

Universal dialogue identity system.

Every dialogue turn must remain connected to:

Character
    ↓
Speaker Identity
    ↓
Language
    ↓
Accent
    ↓
Voice
    ↓
Emotion
    ↓
Delivery
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CharacterIdentity:
    character_id: str
    name: str

    face_reference: str = ""

    appearance: str = ""
    age: str = ""
    gender: str = ""

    hair: str = ""
    eyes: str = ""
    body_type: str = ""

    voice_profile: str = ""

    language: str = ""
    accent: str = ""

    wardrobe_identity: str = ""

    identity_notes: str = ""


@dataclass
class DialogueTurn:
    dialogue_id: str
    speaker_id: str
    line: str

    emotion: str = ""

    language: str = ""
    accent: str = ""
    voice_profile: str = ""

    delivery: str = ""

    previous_dialogue_id: str = ""
    next_dialogue_id: str = ""


@dataclass
class DialogueSequence:
    scene_id: str

    turns: List[DialogueTurn] = field(
        default_factory=list
    )


class DialogueEngine:

    def __init__(self):

        self.characters: Dict[
            str, CharacterIdentity
        ] = {}

        self.sequences: Dict[
            str, DialogueSequence
        ] = {}

    def register_character(
        self,
        character: CharacterIdentity,
    ):

        self.characters[
            character.character_id
        ] = character

    def get_character(
        self,
        character_id: str,
    ) -> Optional[CharacterIdentity]:

        return self.characters.get(
            character_id
        )

    def create_sequence(
        self,
        scene_id: str,
    ) -> DialogueSequence:

        sequence = DialogueSequence(
            scene_id=scene_id
        )

        self.sequences[
            scene_id
        ] = sequence

        return sequence

    def add_dialogue_turn(
        self,
        scene_id: str,
        dialogue_id: str,
        speaker_id: str,
        line: str,
        emotion: str = "",
        delivery: str = "",
    ) -> DialogueTurn:

        character = self.get_character(
            speaker_id
        )

        if character is None:
            raise ValueError(
                f"Unknown speaker: {speaker_id}"
            )

        if not line.strip():
            raise ValueError(
                "Dialogue line cannot be empty."
            )

        sequence = self.sequences.get(
            scene_id
        )

        if sequence is None:
            sequence = self.create_sequence(
                scene_id
            )

        previous_id = ""

        if sequence.turns:
            previous_id = (
                sequence.turns[-1].dialogue_id
            )

        turn = DialogueTurn(
            dialogue_id=dialogue_id,

            speaker_id=speaker_id,

            line=line,

            emotion=emotion,

            language=character.language,

            accent=character.accent,

            voice_profile=(
                character.voice_profile
            ),

            delivery=delivery,

            previous_dialogue_id=previous_id,
        )

        if sequence.turns:
            sequence.turns[-1].next_dialogue_id = (
                dialogue_id
            )

        sequence.turns.append(turn)

        return turn

    def get_sequence(
        self,
        scene_id: str,
    ) -> Optional[DialogueSequence]:

        return self.sequences.get(
            scene_id
        )

    def validate_sequence(
        self,
        scene_id: str,
    ) -> dict:

        sequence = self.get_sequence(
            scene_id
        )

        if sequence is None:
            return {
                "status": "FAIL",
                "errors": [
                    "Dialogue sequence does not exist."
                ],
            }

        errors = []

        for turn in sequence.turns:

            if not turn.speaker_id:
                errors.append(
                    f"{turn.dialogue_id}: "
                    "missing speaker."
                )

            if not turn.line.strip():
                errors.append(
                    f"{turn.dialogue_id}: "
                    "empty dialogue."
                )

            character = self.get_character(
                turn.speaker_id
            )

            if character is None:
                errors.append(
                    f"{turn.dialogue_id}: "
                    f"unknown speaker "
                    f"{turn.speaker_id}."
                )
                continue

            if turn.language != character.language:
                errors.append(
                    f"{turn.dialogue_id}: "
                    "language does not match "
                    "speaker identity."
                )

            if turn.accent != character.accent:
                errors.append(
                    f"{turn.dialogue_id}: "
                    "accent does not match "
                    "speaker identity."
                )

            if (
                turn.voice_profile
                != character.voice_profile
            ):
                errors.append(
                    f"{turn.dialogue_id}: "
                    "voice does not match "
                    "speaker identity."
                )

        if errors:

            return {
                "status": "FAIL",
                "errors": errors,
            }

        return {
            "status": "PASS",
            "errors": [],
        }

    def build_generation_context(
        self,
        scene_id: str,
    ) -> dict:

        sequence = self.get_sequence(
            scene_id
        )

        if sequence is None:
            raise ValueError(
                f"No dialogue sequence "
                f"for scene {scene_id}"
            )

        turns = []

        for turn in sequence.turns:

            character = self.get_character(
                turn.speaker_id
            )

            if character is None:
                raise ValueError(
                    f"Unknown speaker: "
                    f"{turn.speaker_id}"
                )

            turns.append(
                {
                    "dialogue_id":
                        turn.dialogue_id,

                    "speaker_id":
                        character.character_id,

                    "speaker_name":
                        character.name,

                    "line":
                        turn.line,

                    "emotion":
                        turn.emotion,

                    "language":
                        character.language,

                    "accent":
                        character.accent,

                    "voice":
                        character.voice_profile,

                    "delivery":
                        turn.delivery,

                    "previous_dialogue_id":
                        turn.previous_dialogue_id,

                    "next_dialogue_id":
                        turn.next_dialogue_id,
                }
            )

        return {
            "scene_id": scene_id,
            "turn_count": len(turns),
            "turns": turns,
        }
