"""Add Order model

Revision ID: 566d13c2c86b
Revises: ca3b6e97d80b
Create Date: 2024-09-13 23:24:36.635163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '566d13c2c86b'
down_revision: Union[str, None] = 'ca3b6e97d80b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('product_ids', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('RECEIVED', 'PREPARING', 'READY', 'FINISHED', name='orderstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('users', 'cpf',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'cpf',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('orders')
    # ### end Alembic commands ###
