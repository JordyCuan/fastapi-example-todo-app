"""Add phone number column on user table

Revision ID: 27cc31057eb7
Revises: ae58ec5dfe8f
Create Date: 2023-04-13 23:42:39.823002

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "27cc31057eb7"
down_revision = "ae58ec5dfe8f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("phone_number", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "phone_number")
