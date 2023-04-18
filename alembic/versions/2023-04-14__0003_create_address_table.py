"""_0003_Create address table

Revision ID: 73b87d218b69
Revises: 27cc31057eb7
Create Date: 2023-04-14 20:28:23.612850

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "73b87d218b69"
down_revision = "27cc31057eb7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "address",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column("address1", sa.String(), nullable=False),
        sa.Column("address2", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("postal_code", sa.String(), nullable=False),
    )

    op.add_column("user", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "address_users_fk",
        source_table="user",
        referent_table="address",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("address_users_fk", table_name="user")
    op.drop_column("user", "address_id")
    op.drop_table("address")
