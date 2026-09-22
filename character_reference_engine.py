"""
VYDA AI MOVIE ENGINE
Character Reference Engine — Build 016

Purpose:
Create and manage persistent visual references
for every character.

The Character Reference Engine helps preserve:

- Face identity
- Appearance
- Age
- Hair
- Eyes
- Body type
- Wardrobe identity
- Visual notes
- Multiple reference assets

The engine is universal.
It does not assume any country, culture,
language, genre, or visual style.

The user creates the world.
VYDA adapts to it.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CharacterReference:

    character_id: str

    reference_id: str

    reference_type: str = "face"

    asset_location: str = ""

    description: str = ""

    provider: str = ""

    model: str = ""

    seed: str = ""

    notes: str = ""


@dataclass
class CharacterVisualIdentity:

    character_id: str

    name: str

    appearance: str = ""

    age: str = ""

    gender: str = ""

    hair: str = ""

    eyes: str = ""

    body_type: str = ""

    wardrobe_identity: str = ""

    references: List[CharacterReference] = field(
        default_factory=list
    )


class CharacterReferenceEngine:

    def __init__(self):

        self.characters: Dict[
            str,
            CharacterVisualIdentity
        ] = {}

    def register_character(
        self,
        character_id: str,
        name: str,
        appearance: str = "",
        age: str = "",
        gender: str = "",
        hair: str = "",
        eyes: str = "",
        body_type: str = "",
        wardrobe_identity: str = "",
    ) -> CharacterVisualIdentity:

        identity = CharacterVisualIdentity(
            character_id=character_id,
            name=name,
            appearance=appearance,
            age=age,
            gender=gender,
            hair=hair,
            eyes=eyes,
            body_type=body_type,
            wardrobe_identity=wardrobe_identity,
        )

        self.characters[
            character_id
        ] = identity

        return identity

    def add_reference(
        self,
        reference: CharacterReference,
    ):

        if reference.character_id not in self.characters:

            raise ValueError(
                f"Character "
                f"'{reference.character_id}' "
                "is not registered."
            )

        identity = self.characters[
            reference.character_id
        ]

        identity.references.append(
            reference
        )

    def get_identity(
        self,
        character_id: str,
    ) -> CharacterVisualIdentity:

        if character_id not in self.characters:

            raise ValueError(
                f"Character "
                f"'{character_id}' "
                "is not registered."
            )

        return self.characters[
            character_id
        ]

    def get_references(
        self,
        character_id: str,
    ) -> List[CharacterReference]:

        identity = self.get_identity(
            character_id
        )

        return list(
            identity.references
        )

    def build_generation_context(
        self,
        character_id: str,
    ) -> dict:

        identity = self.get_identity(
            character_id
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

            "wardrobe_identity":
                identity.wardrobe_identity,

            "references": [
                {
                    "reference_id":
                        reference.reference_id,

                    "reference_type":
                        reference.reference_type,

                    "asset_location":
                        reference.asset_location,

                    "description":
                        reference.description,

                    "provider":
                        reference.provider,

                    "model":
                        reference.model,

                    "seed":
                        reference.seed,

                    "notes":
                        reference.notes,
                }

                for reference
                in identity.references
            ],
      }
