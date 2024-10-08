"""empty message

Revision ID: 1e5178ebab70
Revises: fcdb5cdce4a2
Create Date: 2024-08-01 12:14:15.192415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e5178ebab70'
down_revision: Union[str, None] = 'fcdb5cdce4a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('fingerprint', sa.String(), nullable=True))
    op.drop_index('ix_users_session_id', table_name='users')
    op.create_index(op.f('ix_users_fingerprint'), 'users', ['fingerprint'], unique=True)
    op.drop_column('users', 'session_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('session_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_fingerprint'), table_name='users')
    op.create_index('ix_users_session_id', 'users', ['session_id'], unique=True)
    op.drop_column('users', 'fingerprint')
    # ### end Alembic commands ###
