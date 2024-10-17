# import json
from collections.abc import Iterator

import nntp
from pydantic import ValidationError

from server.schemas import Card, Channel, ChannelSummary, Metadata, NewCard

DEFAULT_NEWSGROUPS: dict[str, str] = {
    ("control.cancel", "Cancel messages (no posting)"),
    ("control.checkgroups", "Hierarchy check control messages (no posting)"),
    ("control.newgroup", "Newsgroup creation control messages (no posting)"),
    ("control.rmgroup", "Newsgroup removal control messages (no posting)"),
    ("control", "Various control messages (no posting)"),
    ("junk", "Unfiled articles (no posting)"),
    ("local.general", "Local general group"),
    ("local.test", "Local test group"),
}

CLIENT: nntp.NNTPClient | None = None


def get_client() -> nntp.NNTPClient:
    global CLIENT
    CLIENT = CLIENT or nntp.NNTPClient("localhost")
    return CLIENT


def enable_a_default_channel(channel_name: str = "local.test") -> None:
    for name, description in DEFAULT_NEWSGROUPS:
        if name == channel_name:
            DEFAULT_NEWSGROUPS.remove((name, description))
            break
    else:
        msg = f"{channel_name} is not in {DEFAULT_NEWSGROUPS}"
        raise ValueError(msg)


def channels() -> Iterator[Channel]:
    client = get_client()
    for name, description in set(client.list_newsgroups()) - DEFAULT_NEWSGROUPS:
        yield Channel(name=name, description=description)


def channel_summary(channel_name: str) -> ChannelSummary:
    client = get_client()
    est_total, first, last, name = client.group(channel_name)
    return ChannelSummary(
        name=name,
        estimated_total_articles=est_total,
        first_article=first,
        last_article=last,
    )


def _to_metadata(x):
    try:
        return Metadata.model_validate_json(x)
    except ValidationError:
        return x


def channel_cards(channel_name: str, start: int, end: int) -> list[Card]:
    client = get_client()
    _, _first, last, _ = client.group(channel_name)
    if end > last:
        end = last
    return [
        Card(
            number=x[0],
            headers=x[1],
            subject=x[1]["Subject"],
            body=_to_metadata(x[2]),
        )
        for x in [client.article(i) for i in range(start, end + 1)]
    ]


def create_post(card: NewCard):
    client = get_client()
    headers = {
        "Subject": card.subject,
        "From": "OERCommons <admin@oercommons.org>",
        "Newsgroups": ",".join(card.channels),
    }
    t = card.body.model_dump_json()
    return client.post(headers=headers, body=t)


def import_post(channel_name: str, card_id: int) -> bool:  # noqa: ARG001
    return True
