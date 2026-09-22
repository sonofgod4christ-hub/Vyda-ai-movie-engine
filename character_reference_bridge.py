"""
VYDA AI MOVIE ENGINE
Character Reference Bridge — Build 017

Connects the Movie Brain Character Bible
to the Character Reference Engine.

Purpose:
Keep one authoritative character identity
while attaching persistent visual references.

The user creates the world.
VYDA adapts to it.
"""

from typing import List

from movie_brain import Character

from character_reference_engine import (
    CharacterReference,
    CharacterReferenceEngine,
    CharacterVisualIdentity,
)


class CharacterReferenceBridge:

    def __init__(
        self,
        reference_engine: CharacterReferenceEngine,
    ):
        self.reference_engine = reference_engine

    def register_character(
        self,
        character: Character,
    ) -> CharacterVisualIdentity:

        return self.reference_engine.register_character(
            character_id=character.character_id,
            name=character.name,
            appearance=character.appearance,
            age=character.age,
            gender=character.gender,
            hair=character.hair,
            eyes=character.eyes,
            body_type=character.body_type,
            wardrobe_identity=character.wardrobe,
        )

    def register_characters(
        self,
        characters: List[Character],
    ) -> List[CharacterVisualIdentity]:

        identities = []

        for character in characters:

            identity = self.register_character(
                character
            )

            identities.append(
                identity
            )

        return identities

    def add_reference(
        self,
        reference: CharacterReference,
    ):
        self.reference_engine.add_reference(
            reference
        )

    def get_generation_context(
        self,
        character_id: str,
    ) -> dict:

        return (
            self.reference_engine
            .build_generation_context(
                character_id
            )
        )
