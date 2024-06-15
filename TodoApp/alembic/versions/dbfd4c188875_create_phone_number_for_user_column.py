"""Create phone number for user column

Revision ID: dbfd4c188875
Revises: 
Create Date: 2024-06-14 19:32:02.859997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbfd4c188875'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # adding a phone number table, its data type is of string, and then making it so that can take null values
    op.add_column('users', sa.Column('phone_number',sa.String(), nullable=True))

# for deleting and reverting 
def downgrade() -> None:
    # op.drop_column('users', 'phone_number')
    pass
