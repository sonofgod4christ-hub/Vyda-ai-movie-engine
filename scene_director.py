"""
VYDA AI MOVIE ENGINE
Scene Director — Build 009

Converts a movie scene and current continuity state
into a structured production brief.

This is the foundation for future:
- Image generation
- Video generation
- Voice generation
- Lip-sync
- Music
- Sound effects
"""

from dataclasses import dataclass, field
from typing import List

from movie_brain import MoviePlan, Scene
from movie_director import MovieDirector


@dataclass
class SceneProductionBrief:
    """
    Complete production information for one scene.
    """

    scene_id: str

    location_id: str

    time: str

    characters: List[str] = field(default_factory=list)

    action: str = ""

    dialogue: List[str] = field(default_factory=list)

    wardrobe_notes: str = ""

    emotional_state: str = ""

    camera: str = ""

    lighting: str = ""

    duration_seconds: int = 0

    visual_style: str = ""

    cinematic_style: str = ""

    language: str = ""

    dialogue_style: str = ""

    continuity: dict = field(default_factory=dict)


class SceneDirector:
    """
    Prepares individual scenes for production.
    """

    def __init__(
        self,
        movie: MoviePlan,
        director: MovieDirector,
    ):

        self.movie = movie
        self.director = director

    def prepare_scene(
        self,
        scene_id: str,
    ) -> SceneProductionBrief:
        """
        Prepare one scene using the movie's
        creative profile and current continuity.
        """

        scene = self._find_scene(scene_id)

        continuity_context = (
            self.director.prepare_scene(scene_id)
        )

        style = self.movie.creative_style

        return SceneProductionBrief(
            scene_id=scene.scene_id,

            location_id=scene.location_id,

            time=scene.time,

            characters=scene.characters,

            action=scene.action,

            dialogue=scene.dialogue,

            wardrobe_notes=scene.wardrobe_notes,

            emotional_state=scene.emotional_state,

            camera=scene.camera,

            lighting=scene.lighting,

            duration_seconds=scene.duration_seconds,

            visual_style=style.visual_style,

            cinematic_style=style.cinematic_style,

            language=style.language,

            dialogue_style=style.dialogue_style,

            continuity=continuity_context[
                "continuity"
            ],
        )

    def _find_scene(
        self,
        scene_id: str,
    ) -> Scene:

        for scene in self.movie.scenes:

            if scene.scene_id == scene_id:
                return scene

        raise ValueError(
            f"Scene '{scene_id}' was not found."
      )
