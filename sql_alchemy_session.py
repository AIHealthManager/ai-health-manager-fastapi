from typing import TYPE_CHECKING, Protocol, runtime_checkable
import json

if TYPE_CHECKING:
    from agents.items import TResponseInputItem

from agents.memory.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class SQLAlchemySession(Session):
    """SQLAlchemy-based implementation of session storage."""

    def __init__(
        self,
        session_id: str,
        db: AsyncSession,
        sessions_table: str = "agent_sessions",
        messages_table: str = "agents_messages",
    ) -> None:
        self.session_id = session_id
        self.db = db
        self.sessions_table = sessions_table
        self.messages_table = messages_table

    async def _init_db_for_connection(self, db: AsyncSession) -> None:
        """Initialize the database schema for a specific connection."""
        await db.execute(
            text(
                f"""
            CREATE TABLE IF NOT EXISTS {self.sessions_table} (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
            )
        )

        await db.execute(
            text(
                f"""
            CREATE TABLE IF NOT EXISTS {self.messages_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES {self.sessions_table} (session_id)
                    ON DELETE CASCADE
            )
        """
            )
        )

        await db.execute(
            text(
                f"""
            CREATE INDEX IF NOT EXISTS idx_{self.messages_table}_session_id
            ON {self.messages_table} (session_id, created_at)
        """
            )
        )

        await db.commit()

    async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:
        """Retrieve the conversation history for this session.

        Args:
            limit: Maximum number of items to retrieve. If None, retrieves all items.
                   When specified, returns the latest N items in chronological order.

        Returns:
            List of input items representing the conversation history
        """
        if limit is None:
            result = await self.db.execute(text(f"""
                SELECT message_data FROM {self.messages_table}
                WHERE session_id = :session_id
                ORDER BY created_at DESC
            """), {"session_id": self.session_id})
        else:
            result = await self.db.execute(text(f"""
                SELECT message_data FROM {self.messages_table}
                WHERE session_id = :session_id
                ORDER BY created_at DESC
                LIMIT :limit
            """), {"session_id": self.session_id, "limit": limit})

        rows = result.scalars().all()

        items = []
        for (mesage_data,) in rows:
            try:
                item = json.loads(mesage_data)
                items.append(item)
            except json.JSONDecodeError:
                # Skip invalid JSON entries
                continue

        return items

    async def add_items(self, items: list[TResponseInputItem]) -> None:
        """Add new items to the conversation history.

        Args:
            items: List of input items to add to the history
        """
        if not items:
            return
        
        await self.db.execute(text(
            f"INSERT OR IGNORE INTO {self.sessions_table} (session_id) VALUES (:session_id)"
        ), {"session_id": self.session_id})

        message_data = [{"session_id": self.session_id, "message_data": item} for item in items]
        await self.db.execute(text(f"""
            INSERT INTO {self.messages_table} (session_id, message_data) VALUES (:session_id, :message_data)
        """), message_data)

        await self.db.execute(text(f"""
            UPDATE {self.sessions_table}
            SET updated_at = CURRENT_TIMESTAMP
            WHERE session_id = :session_id
        """), {"session_id": self.session_id})

        await self.db.commit()

    async def pop_item(self) -> TResponseInputItem | None:
        """Remove and return the most recent item from the session.

        Returns:
            The most recent item if it exists, None if the session is empty
        """
        