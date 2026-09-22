"""
VYDA AI MOVIE ENGINE
Continuity Engine — Build 005

Purpose:
Keep characters, locations, wardrobe, relationships,
props, timeline, and story state consistent across scenes.

The Continuity Engine is universal.
It does not assume any country, culture, language,
genre, visual style, or character type.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CharacterState:
    """
    Tracks the current state of a character.
    """

    character_id: str
    location_id: str = ""
    wardrobe: str = ""
    emotional_state: str = ""
    physical_state: str = ""
    relationship_state: Dict[str, str] = field(default_factory=dict)
    knowledge: List[str] = field(default_factory=list)


@dataclass
class WorldState:
    """
    Tracks important elements of the movie world.
    """

    current_time: str = ""
    current_location: str = ""

    active_characters: List[str] = field(default_factory=list)

    props: Dict[str, str] = field(default_factory=dict)

    world_facts: List[str] = field(default_factory=list)


class ContinuityEngine:
    """
    Maintains continuity information between scenes.
    """

    def __init__(self):
        self.characters: Dict[str, CharacterState] = {}
        self.world = WorldState()
        self.scene_history: List[str] = []

    def register_character(
        self,
        character_id: str,
        location_id: str = "",
        wardrobe: str = "",
        emotional_state: str = "",
    ):

        self.characters[character_id] = CharacterState(
            character_id=character_id,
            location_id=location_id,
            wardrobe=wardrobe,
            emotional_state=emotional_state,
        )

    def update_character(
        self,
        character_id: str,
        location_id: str = "",
        wardrobe: str = "",
        emotional_state: str = "",
        physical_state: str = "",
    ):

        if character_id not in self.characters:
            self.register_character(character_id)

        character = self.characters[character_id]

        if location_id:
            character.location_id = location_id

        if wardrobe:
            character.wardrobe = wardrobe

        if emotional_state:
            character.emotional_state = emotional_state

        if physical_state:
            character.physical_state = physical_state

    def add_character_knowledge(
        self,
        character_id: str,
        fact: str,
    ):

        if character_id not in self.characters:
            self.register_character(character_id)

        if fact not in self.characters[character_id].knowledge:
            self.characters[character_id].knowledge.append(fact)

    def update_relationship(
        self,
        character_id: str,
        other_character_id: str,
        relationship: str,
    ):

        if character_id not in self.characters:
            self.register_character(character_id)

        self.characters[character_id].relationship_state[
            other_character_id
        ] = relationship

    def update_world(
        self,
        time: str = "",
        location_id: str = "",
    ):

        if time:
            self.world.current_time = time

        if location_id:
            self.world.current_location = location_id

    def add_world_fact(self, fact: str):

        if fact not in self.world.world_facts:
            self.world.world_facts.append(fact)

    def update_prop(
        self,
        prop_name: str,
        state: str,
    ):

        self.world.props[prop_name] = state

    def begin_scene(
        self,
        scene_id: str,
        character_ids: List[str],
        location_id: str,
        time: str = "",
    ):

        self.scene_history.append(scene_id)

        self.world.current_location = location_id

        if time:
            self.world.current_time = time

        self.world.active_characters = character_ids

        for character_id in character_ids:

            if character_id not in self.characters:
                self.register_character(
                    character_id=character_id,
                    location_id=location_id,
                )
            else:
                self.characters[character_id].location_id = location_id

    def get_character_state(
        self,
        character_id: str,
    ) -> CharacterState:

        if character_id not in self.characters:
            raise ValueError(
                f"Character '{character_id}' is not registered."
            )

        return self.characters[character_id]

    def get_world_state(self) -> WorldState:

        return self.world

    def get_continuity_snapshot(self) -> dict:
        """
        Returns a complete snapshot that future AI workers
        can use when generating a scene.
        """

        return {
            "characters": {
                character_id: {
                    "location_id": state.location_id,
                    "wardrobe": state.wardrobe,
                    "emotional_state": state.emotional_state,
                    "physical_state": state.physical_state,
                    "relationships": state.relationship_state,
                    "knowledge": state.knowledge,
                }
                for character_id, state in self.characters.items()
            },
            "world": {
                "current_time": self.world.current_time,
                "current_location": self.world.current_location,
                "active_characters": self.world.active_characters,
                "props": self.world.props,
                "world_facts": self.world.world_facts,
            },
            "scene_history": self.scene_history,
          }
