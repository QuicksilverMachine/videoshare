"""Remove path field

Revision ID: 54d9c94d761b
Revises: 5e1c83b879af
Create Date: 2022-11-07 02:01:32.802190

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "54d9c94d761b"
down_revision = "5e1c83b879af"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index("ix_nodes_path", table_name="nodes")
    op.drop_column("nodes", "path")


def downgrade():
    op.add_column(
        "nodes", sa.Column("path", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.create_index("ix_nodes_path", "nodes", ["path"], unique=False)
