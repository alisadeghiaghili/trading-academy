"""Alembic migration script template."""

# revision identifiers, used by Alembic.
revision = '${rev}'
down_revision = ${down_revision!r}
branch_labels = ${branch_labels!r}
depends_on = ${depends_on!r}

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

${imports if imports else ""}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}