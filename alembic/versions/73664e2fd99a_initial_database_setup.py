"""initial database setup

Revision ID: 73664e2fd99a
Revises: 
Create Date: 2025-01-31 16:22:05.465609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73664e2fd99a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        drop TABLE if exists matches;
        CREATE TABLE matches (
            match_id VARCHAR(50) PRIMARY KEY,      -- Unique match identifier
            game_datetime TIMESTAMP,               -- Timestamp when the game started
            game_length FLOAT,                     -- Duration of the game (in seconds)
            game_version VARCHAR(255),             -- Version of the game
            queue_id INT,                          -- Queue type ID (e.g., ranked, normal)
            end_game_result VARCHAR(50),           -- End result of the game
            game_id BIGINT,                        -- Numeric identifier of the game
            map_id INT                             -- Map identifier
        );
    """)


def downgrade() -> None:
    op.execute("""
    drop TABLE IF EXISTS matches;
    """)
