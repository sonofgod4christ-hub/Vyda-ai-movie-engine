from movie_brain import MovieBrain, Character, Scene


def create_movie():
    brain = MovieBrain()

    movie = brain.create_movie_plan(
        title="The Second Chance",
        logline="A mother gets one opportunity to repair the relationship with her daughter.",
        genre="Drama",
        theme="Family and forgiveness",
        characters=[
            Character(
                character_id="CHAR-001",
                name="Ejiro",
                age="35",
                role="Mother",
                personality=["strong", "loving", "protective"],
            ),
            Character(
                character_id="CHAR-002",
                name="Tega",
                age="15",
                role="Daughter",
                personality=["quiet", "emotional", "intelligent"],
            ),
        ],
        scenes=[
            Scene(
                scene_id="SCENE-001",
                location="Family Living Room",
                time="Evening",
                characters=["CHAR-001", "CHAR-002"],
                action="Ejiro notices that Tega is unusually quiet.",
                dialogue=[
                    "Ejiro: Tega, my daughter, are you okay?",
                    "Tega: I'm fine, Mummy.",
                ],
            )
        ],
    )

    return movie


if __name__ == "__main__":
    movie = create_movie()

    print("VYDA AI MOVIE ENGINE")
    print("====================")
    print()
    print("TITLE:", movie.title)
    print("LOGLINE:", movie.logline)
    print("GENRE:", movie.genre)
    print("THEME:", movie.theme)
    print()
    print("CHARACTERS")
    print("----------")

    for character in movie.characters:
        print(
            f"{character.character_id} | "
            f"{character.name} | "
            f"{character.age} | "
            f"{character.role}"
        )

    print()
    print("SCENES")
    print("------")

    for scene in movie.scenes:
        print(
            f"{scene.scene_id} | "
            f"{scene.location} | "
            f"{scene.time}"
        )
        print("Action:", scene.action)

        for line in scene.dialogue:
            print("Dialogue:", line)
