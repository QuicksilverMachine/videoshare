"""Initial migration

Revision ID: c7a3b7861bcd
Revises:
Create Date: 2022-11-05 17:55:58.209344

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c7a3b7861bcd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "folders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("videos")
    op.drop_table("folders")
