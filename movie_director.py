"""
VYDA AI MOVIE ENGINE
Movie Director — Build 006

Connects the Movie Brain with the Continuity Engine.

The Movie Director coordinates the movie production state.
"""

from movie_brain import MoviePlan
from continuity_engine import ContinuityEngine


class MovieDirector:
    """
    Central director that coordinates:

    Movie Brain
        ↓
    Character Bible
        ↓
    Continuity Engine
        ↓
    Scene Production
    """

    def __init__(self, movie: MoviePlan):

        self.movie = movie
        self.continuity = ContinuityEngine()

        self._initialize_movie()

    def _initialize_movie(self):
        """
        Register all characters and establish their
        initial continuity information.
        """

        for character in self.movie.characters:

            self.continuity.register_character(
                character_id=character.character_id,
                wardrobe=character.wardrobe,
            )

            for relationship in character.relationships:

                self.continuity.add_character_knowledge(
                    character.character_id,
                    relationship,
                )

        for location in self.movie.locations:

            self.continuity.add_world_fact(
                f"Location: {location.name}"
            )

    def prepare_scene(self, scene_id: str):
        """
        Prepare a scene using the current continuity state.
        """

        scene = next(
            (
                scene
                for scene in self.movie.scenes
                if scene.scene_id == scene_id
            ),
            None,
        )

        if scene is None:
            raise ValueError(
                f"Scene '{scene_id}' was not found."
            )

        self.continuity.begin_scene(
            scene_id=scene.scene_id,
            character_ids=scene.characters,
            location_id=scene.location_id,
            time=scene.time,
        )

        return self.get_production_context()

    def get_production_context(self):
        """
        Returns the information that future generation
        workers will need to create the current scene.
        """

        return {
            "movie": {
                "title": self.movie.title,
                "logline": self.movie.logline,
                "theme": self.movie.theme,
            },

            "creative_style": {
                "genre": self.movie.creative_style.genre,
                "tone": self.movie.creative_style.tone,
                "visual_style": self.movie.creative_style.visual_style,
                "cinematic_style": self.movie.creative_style.cinematic_style,
                "language": self.movie.creative_style.language,
                "dialogue_style": self.movie.creative_style.dialogue_style,
                "cultural_style": self.movie.creative_style.cultural_style,
                "era": self.movie.creative_style.era,
                "rating": self.movie.creative_style.rating,
            },

            "continuity": self.continuity.get_continuity_snapshot(),
        }

    def get_continuity(self):
        """
        Returns the current movie continuity state.
        """

        return self.continuity.get_continuity_snapshot()
