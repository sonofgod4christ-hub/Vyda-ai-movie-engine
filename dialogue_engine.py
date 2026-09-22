"""
VYDA AI MOVIE ENGINE
Dialogue & Character Identity Engine — Build 010

Purpose:
- Lock character identity information.
- Assign every dialogue line to a specific character.
- Preserve speaker order.
- Preserve language and accent information.
- Prepare dialogue for future voice and lip-sync workers.

The engine does not assume any country, culture, language,
accent, genre, or character type.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CharacterIdentity:
    """
    Persistent identity package for one character.

    This identity should remain attached to the character
    throughout the entire movie unless the filmmaker
    intentionally changes something.
    """

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
    """
    One individual spoken line.

    speaker_id guarantees that VYDA knows exactly
    who is saying the line.
    """

    dialogue_id: str

    speaker_id: str

    line: str

    emotion: str = ""

    language: str = ""

    accent: str = ""

    delivery: str = ""

    previous_dialogue_id: str = ""

    next_dialogue_id: str = ""


@dataclass
class DialogueSequence:
    """
    Complete conversation sequence for a scene.
    """

    scene_id: str

    turns: List[DialogueTurn] = field(
        default_factory=list
    )


class DialogueEngine:
    """
    Controls character identities and dialogue sequences.
    """

    def __init__(self):

        self.identities: Dict[
            str,
            CharacterIdentity
        ] = {}

        self.sequences: Dict[
            str,
            DialogueSequence
        ] = {}

    def register_character_identity(
        self,
        identity: CharacterIdentity,
    ):

        self.identities[
            identity.character_id
        ] = identity

    def get_character_identity(
        self,
        character_id: str,
    ) -> CharacterIdentity:

        if character_id not in self.identities:

            raise ValueError(
                f"Character identity '{character_id}' "
                "is not registered."
            )

        return self.identities[character_id]

    def create_dialogue_sequence(
        self,
        scene_id: str,
    ) -> DialogueSequence:

        sequence = DialogueSequence(
            scene_id=scene_id
        )

        self.sequences[scene_id] = sequence

        return sequence

    def add_dialogue_turn(
        self,
        scene_id: str,
        dialogue_id: str,
        speaker_id: str,
        line: str,
        emotion: str = "",
        language: str = "",
        accent: str = "",
        delivery: str = "",
    ):

        if speaker_id not in self.identities:

            raise ValueError(
                f"Speaker '{speaker_id}' does not "
                "have a registered character identity."
            )

        if scene_id not in self.sequences:

            self.create_dialogue_sequence(
                scene_id
            )

        sequence = self.sequences[scene_id]

        previous_id = ""

        if sequence.turns:

            previous_id = sequence.turns[-1].dialogue_id

            sequence.turns[-1].next_dialogue_id = (
                dialogue_id
            )

        identity = self.identities[speaker_id]

        dialogue_turn = DialogueTurn(
            dialogue_id=dialogue_id,
            speaker_id=speaker_id,
            line=line,
            emotion=emotion,
            language=(
                language
                or identity.language
            ),
            accent=(
                accent
                or identity.accent
            ),
            delivery=delivery,
            previous_dialogue_id=previous_id,
        )

        sequence.turns.append(
            dialogue_turn
        )

        return dialogue_turn

    def validate_dialogue(
        self,
        scene_id: str,
    ) -> List[str]:
        """
        Checks the dialogue sequence before generation.

        Returns a list of errors.
        An empty list means the sequence passed
        the current validation rules.
        """

        errors = []

        if scene_id not in self.sequences:

            errors.append(
                f"Dialogue sequence '{scene_id}' "
                "does not exist."
            )

            return errors

        sequence = self.sequences[scene_id]

        for turn in sequence.turns:

            if not turn.speaker_id:

                errors.append(
                    f"{turn.dialogue_id}: "
                    "No speaker assigned."
                )

                continue

            if (
                turn.speaker_id
                not in self.identities
            ):

                errors.append(
                    f"{turn.dialogue_id}: "
                    f"Unknown speaker "
                    f"'{turn.speaker_id}'."
                )

            if not turn.line.strip():

                errors.append(
                    f"{turn.dialogue_id}: "
                    "Dialogue line is empty."
                )

        return errors

    def get_sequence(
        self,
        scene_id: str,
    ) -> DialogueSequence:

        if scene_id not in self.sequences:

            raise ValueError(
                f"Dialogue sequence '{scene_id}' "
                "does not exist."
            )

        return self.sequences[scene_id]

    def get_generation_context(
        self,
        scene_id: str,
    ) -> dict:
        """
        Creates the structured information that future
        voice, lip-sync, image and video workers can use.
        """

        errors = self.validate_dialogue(
            scene_id
        )

        if errors:

            raise ValueError(
                "Dialogue validation failed: "
                + " | ".join(errors)
            )

        sequence = self.get_sequence(
            scene_id
        )

        turns = []

        for turn in sequence.turns:

            identity = self.get_character_identity(
                turn.speaker_id
            )

            turns.append(
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

                    "language":
                        turn.language,

                    "accent":
                        turn.accent,

                    "delivery":
                        turn.delivery,

                    "voice_profile":
                        identity.voice_profile,

                    "face_reference":
                        identity.face_reference,
                }
            )

        return {
            "scene_id": scene_id,
            "dialogue": turns,
  }
