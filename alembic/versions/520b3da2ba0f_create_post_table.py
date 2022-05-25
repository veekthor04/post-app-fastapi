"""create post table

Revision ID: 520b3da2ba0f
Revises: 
Create Date: 2022-05-25 02:50:13.474457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "520b3da2ba0f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
