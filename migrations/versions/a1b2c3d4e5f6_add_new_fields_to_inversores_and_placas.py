"""add new fields to inversores and placas

Revision ID: a1b2c3d4e5f6
Revises: 2545bf14df22
Create Date: 2026-04-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '2545bf14df22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add STRING_HYBRID to tipo_inversor enum (PostgreSQL only)
    op.execute("ALTER TYPE tipo_inversor ADD VALUE IF NOT EXISTS 'STRING_HYBRID'")

    # Make tipo_de_inversor nullable in inversores
    op.alter_column('inversores', 'tipo_de_inversor', nullable=True)

    # Add new columns to inversores
    op.add_column('inversores', sa.Column('strings_por_mppt', sa.Integer(), nullable=True))
    op.add_column('inversores', sa.Column('total_strings', sa.Integer(), nullable=True))

    # Make tipo_celula nullable in placas
    op.alter_column('placas', 'tipo_celula', nullable=True)

    # Add new columns to placas
    op.add_column('placas', sa.Column('rendimento_ano_1', sa.Float(), nullable=True))
    op.add_column('placas', sa.Column('rendimento_ano_25', sa.Float(), nullable=True))
    op.add_column('placas', sa.Column('peso', sa.Float(), nullable=True))
    op.add_column('placas', sa.Column('largura', sa.Float(), nullable=True))
    op.add_column('placas', sa.Column('altura', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('placas', 'altura')
    op.drop_column('placas', 'largura')
    op.drop_column('placas', 'peso')
    op.drop_column('placas', 'rendimento_ano_25')
    op.drop_column('placas', 'rendimento_ano_1')
    op.alter_column('placas', 'tipo_celula', nullable=False)

    op.drop_column('inversores', 'total_strings')
    op.drop_column('inversores', 'strings_por_mppt')
    op.alter_column('inversores', 'tipo_de_inversor', nullable=False)
