"""create player table
;


Revision ID: 95942253bd8a
Revises: e6de7426e91d
Create Date: 2025-02-06 15:49:19.013754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95942253bd8a'
down_revision: Union[str, None] = 'e6de7426e91d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS player;
        CREATE TABLE player (
            id SERIAL PRIMARY KEY,
            puuid VARCHAR(255),
            queue VARCHAR(255),
            tier VARCHAR(255),
            division VARCHAR(255),
            api_response JSON,
            create_at timestamp DEFAULT NOW()
        );
        """)

def downgrade() -> None:
    op.execute("""
        drop TABLE IF EXISTS player;
    """)
