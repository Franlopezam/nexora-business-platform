# Database

Nexora currently creates its development schema automatically through SQLAlchemy.

For a production project, schema changes should be managed with Alembic. The current model layout intentionally keeps that migration step straightforward.
