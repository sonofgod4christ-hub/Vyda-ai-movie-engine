"""
VYDA AI MOVIE ENGINE
Identity Bridge — Build 031

Connects the Movie Brain Character Bible
to the Dialogue Engine.

One character identity must remain consistent
across the entire production.

Character
    ↓
Appearance
    ↓
Language
    ↓
Accent
    ↓
Voice
    ↓
Wardrobe
    ↓
Dialogue
"""

from movie_brain import Character
from dialogue_engine import (
    CharacterIdentity,
    DialogueEngine,
)


class IdentityBridge:

    def __init__(
        self,
        dialogue_engine: DialogueEngine,
    ):

        self.dialogue_engine = dialogue_engine

    def register_character(
        self,
        character: Character,
    ) -> CharacterIdentity:

        identity = CharacterIdentity(
            character_id=character.character_id,

            name=character.name,

            appearance=character.appearance,

            age=character.age,

            gender=character.gender,

            hair=character.hair,

            eyes=character.eyes,

            body_type=character.body_type,

            language=character.language,

            accent=character.accent,

            voice_profile=character.voice,

            wardrobe_identity=character.wardrobe,

            identity_notes=character.notes,
        )

        self.dialogue_engine.register_character(
            identity
        )

        return identity

    def register_characters(
        self,
        characters: list[Character],
    ) -> list[CharacterIdentity]:

        identities = []

        for character in characters:

            identities.append(
                self.register_character(
                    character
                )
            )

        return identities

    def get_identity(
        self,
        character_id: str,
    ):

        return self.dialogue_engine.get_character(
            character_id
        )

    def build_identity_context(
        self,
        character_id: str,
    ) -> dict:

        identity = self.get_identity(
            character_id
        )

        if identity is None:
            raise ValueError(
                f"Character identity not found: "
                f"{character_id}"
            )

        return {
            "character_id":
                identity.character_id,

            "name":
                identity.name,

            "appearance":
                identity.appearance,

            "age":
                identity.age,

            "gender":
                identity.gender,

            "hair":
                identity.hair,

            "eyes":
                identity.eyes,

            "body_type":
                identity.body_type,

            "language":
                identity.language,

            "accent":
                identity.accent,

            "voice":
                identity.voice_profile,

            "wardrobe":
                identity.wardrobe_identity,

            "identity_notes":
                identity.identity_notes,
        }
