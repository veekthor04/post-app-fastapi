"""add content column to post table

Revision ID: e07c31d5874b
Revises: 520b3da2ba0f
Create Date: 2022-05-25 03:00:32.634919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e07c31d5874b"
down_revision = "520b3da2ba0f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
