"""init

Revision ID: 9107fcb60007
Revises:
Create Date: 2024-09-10 13:23:37.275537

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9107fcb60007"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    role_table = op.create_table(
        "role",
        sa.Column("name", sa.String(length=16), nullable=False),
        sa.Column("permission", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "token",
        sa.Column("cg_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(length=16), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_table(
        "crypto_transaction",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("token_1_id", sa.Integer(), nullable=False),
        sa.Column("token_2_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column(
            "operation", sa.Enum("BUY", "SELL", name="operationenum"), nullable=False
        ),
        sa.Column("price_in_usd", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["token_1_id"], ["token.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["token_2_id"], ["token.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "refresh_token",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=False),
        sa.Column("fingerprint", sa.String(length=250), nullable=False),
        sa.Column("should_deleted_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("refresh_token"),
    )
    op.bulk_insert(
        role_table,
        [
            {
                "name": "admin",
                "permission": {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "name": "user",
                "permission": {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("refresh_token")
    op.drop_table("crypto_transaction")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("token")
    op.drop_table("role")

    op.execute("DELETE FROM role WHERE name IN ('admin', 'user')")
    # ### end Alembic commands ###
