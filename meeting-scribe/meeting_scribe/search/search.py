"""Knowledge-base search across every meeting's transcript and summary."""

from dataclasses import dataclass
from typing import List

from ..storage import Database

SOURCE_LABELS = {"transcript": "逐字稿", "summary": "摘要"}


@dataclass
class SearchHit:
    meeting_id: int
    title: str
    created_at: str
    source_type: str
    snippet: str


def search_meetings(db: Database, query: str, limit: int = 20) -> List[SearchHit]:
    raw_hits = db.search(query, limit=limit)
    hits = []
    for hit in raw_hits:
        meeting = db.get_meeting(hit["meeting_id"])
        hits.append(
            SearchHit(
                meeting_id=hit["meeting_id"],
                title=hit["title"],
                created_at=meeting.created_at if meeting else "",
                source_type=hit["source_type"],
                snippet=hit["snippet"],
            )
        )
    return hits
