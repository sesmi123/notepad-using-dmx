from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Note:
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
