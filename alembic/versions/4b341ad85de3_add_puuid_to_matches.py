"""add puuid to matches

Revision ID: 4b341ad85de3
Revises: 95942253bd8a
Create Date: 2025-02-08 21:10:46.521549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b341ad85de3'
down_revision: Union[str, None] = '95942253bd8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""ALTER TABLE matches add column puuids varchar(255)[]""")

def downgrade() -> None:
    op.execute("alter table matches drop column puuids")
