"""
VYDA AI MOVIE ENGINE
Identity Bridge — Build 011

Connects the Movie Brain Character Bible
to the Dialogue & Character Identity Engine.

Purpose:
Keep one authoritative identity for every character.
"""

from typing import List

from movie_brain import Character

from dialogue_engine import (
    CharacterIdentity,
    DialogueEngine,
)


class IdentityBridge:
    """
    Converts Movie Brain characters into persistent
    Character Identity packages.
    """

    def __init__(
        self,
        dialogue_engine: DialogueEngine,
    ):

        self.dialogue_engine = dialogue_engine

    def register_character(
        self,
        character: Character,
        face_reference: str = "",
    ) -> CharacterIdentity:
        """
        Convert a Movie Brain Character into a
        persistent CharacterIdentity.
        """

        identity = CharacterIdentity(
            character_id=character.character_id,

            name=character.name,

            face_reference=face_reference,

            appearance=character.appearance,

            age=character.age,

            gender=character.gender,

            hair=character.hair,

            eyes=character.eyes,

            body_type=character.body_type,

            voice_profile=character.voice,

            language="",

            accent=character.accent,

            wardrobe_identity=character.wardrobe,

            identity_notes=character.notes,
        )

        self.dialogue_engine.register_character_identity(
            identity
        )

        return identity

    def register_characters(
        self,
        characters: List[Character],
    ) -> List[CharacterIdentity]:
        """
        Register all movie characters.
        """

        identities = []

        for character in characters:

            identity = self.register_character(
                character
            )

            identities.append(identity)

        return identities

    def get_identity(
        self,
        character_id: str,
    ) -> CharacterIdentity:

        return self.dialogue_engine.get_character_identity(
            character_id
  )
