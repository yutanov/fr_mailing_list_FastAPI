"""init

Revision ID: f80c1a95e26d
Revises: 
Create Date: 2022-08-01 07:33:29.110139

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'f80c1a95e26d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phone_operator_code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('tag', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('timezone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mailings',
    sa.Column('sending_start_date', sa.DateTime(), nullable=False),
    sa.Column('sending_end_date', sa.DateTime(), nullable=False),
    sa.Column('message_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('client_filter_json', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logs_clients',
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('action', sa.Integer(), nullable=False),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('data_json', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logs_mailings',
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('action', sa.Integer(), nullable=False),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('data_json', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('mailing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mailing_id'], ['mailings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('send_status', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('mailing_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['mailing_id'], ['mailings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.create_table('logs_messages',
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('action', sa.Integer(), nullable=False),
    sa.Column('data_json', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs_messages')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_table('logs_mailings')
    op.drop_table('logs_clients')
    op.drop_table('mailings')
    op.drop_table('clients')
    # ### end Alembic commands ###
