"""empty message

Revision ID: 3bf5ddf99ec3
Revises:
Create Date: 2022-11-06 17:16:33.862137

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3bf5ddf99ec3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nodes",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("parent_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ("parent_id",),
            ("nodes.id",),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uix_unique_name_type_parent_id",
        "nodes",
        ["name", "type", "parent_id"],
        unique=True,
        postgresql_where=sa.text("parent_id IS NOT NULL"),
    )
    op.create_index(
        "uix_unique_name_type_parent_id_null",
        "nodes",
        ["name", "type", "parent_id"],
        unique=True,
        postgresql_where=sa.text("parent_id IS NULL"),
    )


def downgrade():
    op.drop_index(
        "uix_unique_name_type_parent_id_null",
        table_name="nodes",
        postgresql_where=sa.text("parent_id IS NULL"),
    )
    op.drop_index(
        "uix_unique_name_type_parent_id",
        table_name="nodes",
        postgresql_where=sa.text("parent_id IS NOT NULL"),
    )
    op.drop_table("nodes")
