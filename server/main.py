from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server import ome_node
from server.helpers import MocAPI
from server.schemas import Card, CardRef, Channel, ChannelSummary, NewCard

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://.*\\.localhost:5001",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/list")
async def main() -> list[Channel]:
    return ome_node.channels()


@app.get("/api/channel/{name}")
async def get_channel_summary(name: str) -> ChannelSummary:
    return ome_node.channelSummary(name)


@app.get("/api/channel/{name}/cards")
async def get_channel_cards(name: str, start: int = 1, end: int = 10) -> list[Card]:
    return ome_node.channelCards(name, start, end)


@app.post("/api/publish")
async def create_post(card: NewCard):
    return ome_node.createPost(card)


@app.post("/api/channel/{name}/import")
async def import_post(name: str, card: CardRef) -> bool:
    return ome_node.importPost(name, card.id)


app.mount(
    "/api/imls/",
    MocAPI(directory="static/api/imls/", html=True),
    name="Mock API",
)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
