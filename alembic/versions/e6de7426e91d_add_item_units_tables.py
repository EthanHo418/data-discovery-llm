"""add item units tables

Revision ID: e6de7426e91d
Revises: c8bbe2372394
Create Date: 2025-01-31 16:29:35.810124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e6de7426e91d'
down_revision: Union[str, None] = 'c8bbe2372394'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS item;
    CREATE TABLE item (
        match_id VARCHAR(255),       -- Unique match identifier
        puuid VARCHAR(255),       -- Unique match identifier
        unit_name VARCHAR(255),       -- Unique match identifier
        identifier INT,
        name VARCHAR(255)
    );

    DROP TABLE IF EXISTS unit;
    CREATE TABLE unit (
        match_id VARCHAR(255),       -- Unique match identifier
        puuid VARCHAR(255),       -- Unique match identifier
        name VARCHAR(255),       -- Unique match identifier
        identifier INT,
        rarity INT,
        tier INT
    );
    """
    )


def downgrade() -> None:
    op.execute("""
    drop TABLE IF EXISTS item;
    drop TABLE IF EXISTS unit;
    """
    )
