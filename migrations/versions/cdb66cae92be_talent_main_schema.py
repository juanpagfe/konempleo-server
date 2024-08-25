"""talent main schema

Revision ID: cdb66cae92be
Revises: 
Create Date: 2024-08-25 14:09:57.002330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdb66cae92be'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'company', name='role_enum'), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('companies', sa.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('KAM', sa.String(), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.Column('responsible', sa.String(), nullable=True),
    sa.Column('responsibleMail', sa.String(), nullable=True),
    sa.Column('activeoffers', sa.Integer(), nullable=True),
    sa.Column('totaloffers', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cargo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cvitae',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('size', sa.Float(), nullable=True),
    sa.Column('extension', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('candidate_dni', sa.String(), nullable=True),
    sa.Column('candidate_dni_type', sa.String(), nullable=True),
    sa.Column('candidate_name', sa.String(), nullable=True),
    sa.Column('candidate_phone', sa.String(), nullable=True),
    sa.Column('candidate_mail', sa.String(), nullable=True),
    sa.Column('candidate_city', sa.String(), nullable=True),
    sa.Column('background_check', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('duties', sa.String(), nullable=True),
    sa.Column('exp_area', sa.String(), nullable=True),
    sa.Column('vacants', sa.Integer(), nullable=True),
    sa.Column('contract_type', sa.Enum('full_time', 'part_time', name='contract_type_enum'), nullable=True),
    sa.Column('salary', sa.String(), nullable=True),
    sa.Column('city', sa.Integer(), nullable=True),
    sa.Column('shift', sa.Enum('morning', 'evening', 'night', name='shift_enum'), nullable=True),
    sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender_enum'), nullable=True),
    sa.Column('military_notebook', sa.Enum('yes', 'no', name='military_notebook_enum'), nullable=True),
    sa.Column('age', sa.String(), nullable=True),
    sa.Column('job_type', sa.String(), nullable=True),
    sa.Column('license', sa.Enum('required', 'not_required', name='license_enum'), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('experience_years', sa.Integer(), nullable=True),
    sa.Column('offer_type', sa.String(), nullable=True),
    sa.Column('ed_required', sa.Enum('none', 'high_school', 'bachelor', 'master', 'doctorate', name='ed_required_enum'), nullable=True),
    sa.Column('cargoId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cargoId'], ['cargo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companyUsers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('companyId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['company.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companyOffers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('companyId', sa.Integer(), nullable=False),
    sa.Column('offerId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['company.id'], ),
    sa.ForeignKeyConstraint(['offerId'], ['offers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cargoSkills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cargoId', sa.Integer(), nullable=False),
    sa.Column('skillId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargoId'], ['cargo.id'], ),
    sa.ForeignKeyConstraint(['skillId'], ['skills.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offerSkills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('offerId', sa.Integer(), nullable=False),
    sa.Column('skillId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offerId'], ['offers.id'], ),
    sa.ForeignKeyConstraint(['skillId'], ['skills.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vitaeOffer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cvitaeId', sa.Integer(), nullable=False),
    sa.Column('offerId', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'accepted', 'rejected', name='status_enum'), nullable=True),
    sa.Column('ai_response', sa.Text(), nullable=True),
    sa.Column('response_score', sa.Float(), nullable=True),
    sa.Column('whatsapp_status', sa.Enum('sent', 'delivered', 'read', name='whatsapp_status_enum'), nullable=True),
    sa.ForeignKeyConstraint(['cvitaeId'], ['cvitae.Id'], ),
    sa.ForeignKeyConstraint(['offerId'], ['offers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('vitaeOffer')
    op.drop_table('offerSkills')
    op.drop_table('cargoSkills')
    op.drop_table('companyOffers')
    op.drop_table('companyUsers')
    op.drop_table('offers')
    op.drop_table('cvitae')
    op.drop_table('cargo')
    op.drop_table('skills')
    op.drop_table('company')
    op.drop_table('users')
