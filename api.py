from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="VYDA AI Movie Engine",
    description="The API foundation for the VYDA AI filmmaking system.",
    version="0.1.0",
)


class StoryRequest(BaseModel):
    story_idea: str


@app.get("/")
def home():
    return {
        "engine": "VYDA AI Movie Engine",
        "status": "online",
        "version": "0.1.0",
    }


@app.post("/story")
def receive_story(request: StoryRequest):
    return {
        "received": True,
        "story_idea": request.story_idea,
        "message": "Story received by the VYDA Movie Brain.",
    }
