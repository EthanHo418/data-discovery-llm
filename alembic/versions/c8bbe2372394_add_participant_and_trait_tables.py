"""add participant and trait tables

Revision ID: c8bbe2372394
Revises: 73664e2fd99a
Create Date: 2025-01-31 16:27:02.352873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c8bbe2372394'
down_revision: Union[str, None] = '73664e2fd99a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    drop table if exists participants;
    CREATE TABLE participants (
        match_id VARCHAR(255),       -- Unique match identifier
        puuid VARCHAR(255),       -- Unique match identifier
        game_name varchar(255),
        tag_line varchar(255),
        partner_group INT,
        companion VARCHAR(255),       -- Unique match identifier
        gold_left INT,
        placement INT,
        win BOOLEAN,
        PRIMARY KEY(match_id, puuid)
    );

    DROP TABLE IF EXISTS trait;
    CREATE TABLE trait (
        match_id VARCHAR(255),       -- Unique match identifier
        puuid VARCHAR(255),       -- Unique match identifier
        name VARCHAR(255),       -- Unique match identifier
        num_units INT,
        style INT,
        tier_current INT,
        tier_total INT,
        PRIMARY KEY(match_id, puuid, name)
    );
    """)


def downgrade() -> None:
    op.execute("""
    drop TABLE IF EXISTS participants;
    drop TABLE IF EXISTS trait;
    """)
