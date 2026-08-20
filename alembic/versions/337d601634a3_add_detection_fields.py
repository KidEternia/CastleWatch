"""add detection fields

Revision ID: 337d601634a3
Revises: 43b8620736d1
Create Date: 2026-08-20

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "337d601634a3"
down_revision: Union[str, Sequence[str], None] = "43b8620736d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Existing security events need a value when this NOT NULL
    # column is introduced, so temporarily provide a database default.
    op.add_column(
        "security_events",
        sa.Column(
            "risk_score",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )

    op.add_column(
        "security_events",
        sa.Column(
            "detection_name",
            sa.String(length=150),
            nullable=True,
        ),
    )

    # New events should receive their risk score from CastleWatch's
    # detection engine rather than relying on a permanent DB default.
    op.alter_column(
        "security_events",
        "risk_score",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "security_events",
        "detection_name",
    )

    op.drop_column(
        "security_events",
        "risk_score",
    )