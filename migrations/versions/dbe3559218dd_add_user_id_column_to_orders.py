"""Add user_id column to orders

Revision ID: dbe3559218dd
Revises: 38f403e4efac
Create Date: 2025-09-09 21:34:45.919493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbe3559218dd'
down_revision: Union[str, Sequence[str], None] = '38f403e4efac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with SQLite batch mode."""
    # Alteração em order_items
    with op.batch_alter_table("order_items") as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=True))
        batch_op.drop_column('order')
        batch_op.create_foreign_key("fk_order_items_orders", "orders", ["order_id"], ["id"])

    # Alteração em orders
    with op.batch_alter_table("orders") as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.drop_column('user')
        batch_op.create_foreign_key("fk_orders_users", "users", ["user_id"], ["id"])

    # Criação de constraint única em users
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_unique_constraint("uq_users_email", ["email"])


def downgrade() -> None:
    """Downgrade schema with SQLite batch mode."""
    # Reverter constraint única
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_email", type_="unique")

    # Reverter orders
    with op.batch_alter_table("orders") as batch_op:
        batch_op.drop_constraint("fk_orders_users", type_="foreignkey")
        batch_op.drop_column('user_id')
        batch_op.add_column(sa.Column('user', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "users", ["user"], ["id"])

    # Reverter order_items
    with op.batch_alter_table("order_items") as batch_op:
        batch_op.drop_constraint("fk_order_items_orders", type_="foreignkey")
        batch_op.drop_column('order_id')
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "orders", ["order"], ["id"])