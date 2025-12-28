"""add unaccent extension and index

Revision ID: c3d77a94abc6
Revises: 54c80f6bdfd2
Create Date: 2025-11-02 19:14:25.329870

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "c3d77a94abc6"
down_revision = "54c80f6bdfd2"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")

    op.execute(
        """
        CREATE OR REPLACE FUNCTION immutable_unaccent(text)
        RETURNS text AS $$
        SELECT unaccent($1)
        $$ LANGUAGE sql IMMUTABLE;
    """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_episode_unaccent_title
        ON episode (immutable_unaccent(title));
    """
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_episode_unaccent_title;")
    op.execute("DROP FUNCTION IF EXISTS immutable_unaccent(text);")
    op.execute("DROP EXTENSION IF EXISTS unaccent;")
