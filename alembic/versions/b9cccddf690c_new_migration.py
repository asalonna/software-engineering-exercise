"""New Migration

Revision ID: b9cccddf690c
Revises: 
Create Date: 2023-06-23 11:21:41.359684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9cccddf690c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code_body', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_code_id'), 'code', ['id'], unique=False)
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sibling_id', sa.Integer(), nullable=True),
    sa.Column('message_type', sa.Enum('question', 'response', name='type'), nullable=True),
    sa.Column('message_body', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['sibling_id'], ['message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=False)
    op.create_table('assigned codes',
    sa.Column('assigned_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('code_id', sa.Integer(), nullable=True),
    sa.Column('assigned_substring', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['code_id'], ['code.id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.PrimaryKeyConstraint('assigned_id')
    )
    op.create_index(op.f('ix_assigned codes_assigned_id'), 'assigned codes', ['assigned_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assigned codes_assigned_id'), table_name='assigned codes')
    op.drop_table('assigned codes')
    op.drop_index(op.f('ix_message_id'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_code_id'), table_name='code')
    op.drop_table('code')
    # ### end Alembic commands ###
