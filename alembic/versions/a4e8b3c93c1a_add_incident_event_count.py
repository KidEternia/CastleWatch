"""add incident event count

Revision ID: a4e8b3c93c1a
Revises: b3d42b10f470

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4e8b3c93c1a"

down_revision: Union[str, Sequence[str], None] = "b3d42b10f470"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "incidents",
        sa.Column(
            "event_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
    )

    op.alter_column(
        "incidents",
        "event_count",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "incidents",
        "event_count",
    )