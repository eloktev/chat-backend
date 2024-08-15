"""Add user identifying params

Revision ID: ac12df291a1f
Revises: cecfc368d2db
Create Date: 2024-08-14 23:40:46.138751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac12df291a1f'
down_revision: Union[str, None] = 'cecfc368d2db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
