"""initial

Revision ID: cc1106a70e10
Revises: 
Create Date: 2024-07-30 11:30:22.574861

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "cc1106a70e10"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("idx_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("fki_г", table_name="words")
    op.drop_table("words")


def downgrade() -> None:
    op.create_table(
        "words",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("word", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("definition", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_learned",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "cards",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "word_translation",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "constructor",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "word_audio",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="user_id"),
        sa.PrimaryKeyConstraint("id", name="words_pkey"),
    )
    op.create_index("fki_г", "words", ["user_id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            "username", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column("email", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("password", sa.TEXT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)
