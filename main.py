"""
VYDA AI MOVIE ENGINE
Main Demo — Build 026

Universal architecture demonstration.

This file provides a small internal example
of how the current VYDA Movie Brain works.

It is not tied to any country, culture,
language, genre, or character type.

The user creates the world.
VYDA adapts to it.
"""

from movie_brain import (
    MovieBrain,
    CreativeStyle,
    Character,
    Location,
    Scene,
)


def create_movie():

    brain = MovieBrain()

    creative_style = CreativeStyle(
        genre="Drama",
        tone="Emotional and cinematic",
        visual_style="Natural cinematic realism",
        cinematic_style="Contemporary feature film",
        language="English",
        dialogue_style="Natural conversational dialogue",
        cultural_style="User defined",
        era="Present day",
        rating="General",
    )

    characters = [
        Character(
            character_id="CHAR-001",
            name="Character One",
            age="Adult",
            gender="",
            background="",
            appearance="",
            hair="",
            eyes="",
            body_type="",
            wardrobe="",
            personality=[
                "determined",
                "caring",
            ],
            voice="",
            accent="",
            relationships=[
                "CHAR-002: close relationship",
            ],
            notes="",
        ),

        Character(
            character_id="CHAR-002",
            name="Character Two",
            age="Young adult",
            gender="",
            background="",
            appearance="",
            hair="",
            eyes="",
            body_type="",
            wardrobe="",
            personality=[
                "thoughtful",
                "emotional",
            ],
            voice="",
            accent="",
            relationships=[
                "CHAR-001: close relationship",
            ],
            notes="",
        ),
    ]

    locations = [
        Location(
            location_id="LOC-001",
            name="Main Location",
            description="A user-defined story location.",
            country_or_world="User defined",
            era="Present day",
            visual_style="Cinematic realism",
            notes="",
        )
    ]

    scenes = [
        Scene(
            scene_id="SCENE-001",
            location_id="LOC-001",
            time="Evening",
            characters=[
                "CHAR-001",
                "CHAR-002",
            ],
            wardrobe_notes="",
            emotional_state="Tense but emotional",
            action=(
                "Character One notices that "
                "Character Two is unusually quiet."
            ),
            dialogue=[
                "Character One speaks.",
                "Character Two responds.",
            ],
            camera="Medium shot followed by close-up.",
            lighting="Soft evening lighting.",
            duration_seconds=10,
            previous_scene_id="",
            next_scene_id="",
            continuity_notes="",
        )
    ]

    movie = brain.create_movie_plan(
        title="VYDA Demo Film",
        logline=(
            "Two characters face an emotional "
            "moment that changes their relationship."
        ),
        theme="Human connection",
        creative_style=creative_style,
        characters=characters,
        locations=locations,
        scenes=scenes,
    )

    return movie


if __name__ == "__main__":

    movie = create_movie()

    print("VYDA AI MOVIE ENGINE")
    print("====================")
    print()

    print("TITLE:", movie.title)
    print("LOGLINE:", movie.logline)
    print("THEME:", movie.theme)
    print(
        "GENRE:",
        movie.creative_style.genre,
    )

    print()
    print("CHARACTERS")
    print("----------")

    for character in movie.characters:

        print(
            f"{character.character_id} | "
            f"{character.name} | "
            f"{character.age}"
        )

    print()
    print("LOCATIONS")
    print("---------")

    for location in movie.locations:

        print(
            f"{location.location_id} | "
            f"{location.name}"
        )

    print()
    print("SCENES")
    print("------")

    for scene in movie.scenes:

        print(
            f"{scene.scene_id} | "
            f"{scene.location_id} | "
            f"{scene.time}"
        )

        print(
            "Characters:",
            ", ".join(scene.characters),
        )

        print(
            "Action:",
            scene.action,
        )

        for line in scene.dialogue:

            print(
                "Dialogue:",
                line,
            )
