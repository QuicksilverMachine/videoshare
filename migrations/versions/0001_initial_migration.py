"""Initial migration

Revision ID: 5e1c83b879af
Revises:
Create Date: 2022-11-06 21:45:56.185476

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5e1c83b879af"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nodes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("path", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ("parent_id",),
            ("nodes.id",),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_nodes_path"), "nodes", ["path"], unique=False)
    op.create_index(
        "uix_unique_name_type_parent_id",
        "nodes",
        ["name", "parent_id"],
        unique=True,
        postgresql_where=sa.text("parent_id IS NOT NULL"),
    )
    op.create_index(
        "uix_unique_name_type_parent_id_null",
        "nodes",
        ["name"],
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
    op.drop_index(op.f("ix_nodes_path"), table_name="nodes")
    op.drop_table("nodes")
