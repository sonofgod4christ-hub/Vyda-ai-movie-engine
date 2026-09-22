"""
VYDA AI MOVIE ENGINE
Story Pipeline — Build 008

Converts universal story input into the internal
VYDA movie production structure.

No external AI provider is connected yet.
"""

from typing import List

from movie_brain import (
    MovieBrain,
    MoviePlan,
    CreativeStyle,
    Character,
    Location,
    Scene,
)

from movie_director import MovieDirector


class StoryPipeline:
    """
    Main pipeline for turning filmmaker input into
    a structured VYDA movie plan.
    """

    def __init__(self):

        self.brain = MovieBrain()

    def build_movie(
        self,
        title: str,
        story_idea: str,
        theme: str,
        creative_style: CreativeStyle,
        characters: List[Character],
        locations: List[Location],
        scenes: List[Scene],
    ) -> MoviePlan:
        """
        Build a complete internal movie plan.
        """

        movie = self.brain.create_movie_plan(
            title=title,
            logline=story_idea,
            theme=theme,
            creative_style=creative_style,
            characters=characters,
            locations=locations,
            scenes=scenes,
        )

        return movie

    def create_director(
        self,
        movie: MoviePlan,
    ) -> MovieDirector:
        """
        Create a Movie Director for the movie.

        The director connects the movie plan
        to the Continuity Engine.
        """

        return MovieDirector(movie)

    def build_production_context(
        self,
        movie: MoviePlan,
    ) -> dict:
        """
        Prepare the movie for future production workers.
        """

        director = self.create_director(movie)

        return director.get_production_context()
