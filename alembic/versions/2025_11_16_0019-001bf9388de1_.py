"""empty message

Revision ID: 001bf9388de1
Revises: ef3f5700cb4a
Create Date: 2025-11-16 00:19:30.658785

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001bf9388de1"
down_revision: Union[str, Sequence[str], None] = "ef3f5700cb4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
