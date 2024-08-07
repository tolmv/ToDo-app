"""Initial migration

Revision ID: 2b28a2195782
Revises: 56c2ec130c2e
Create Date: 2024-08-07 19:55:21.238774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b28a2195782'
down_revision = '56c2ec130c2e'
branch_labels = None
depends_on = None


def upgrade():
    # Create the 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username', name='uq_users_username')
    )

    # Create the 'todos' table
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the 'user_todo_permissions' table
    op.create_table(
        'user_todo_permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('todo_id', sa.Integer(), nullable=True),
        sa.Column('can_read', sa.Boolean(), nullable=True, default=False),
        sa.Column('can_update', sa.Boolean(), nullable=True, default=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['todo_id'], ['todos.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop the 'user_todo_permissions' table
    op.drop_table('user_todo_permissions')

    # Drop the 'todos' table
    op.drop_table('todos')

    # Drop the 'users' table
    op.drop_table('users')
