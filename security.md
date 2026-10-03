# Security notes

Nexora includes:

- bcrypt password hashing
- signed JWT access and refresh tokens
- role checks
- basic request rate limiting
- server-side validation through Pydantic
- audit logging for important mutations

Before production:

1. Set a strong random `SECRET_KEY`.
2. Restrict CORS to trusted origins.
3. Put the API behind HTTPS.
4. Replace the demo credentials.
5. Use PostgreSQL.
6. Add persistent refresh-token revocation.
7. Replace the in-memory rate limiter with a shared store such as Redis.
8. Add Alembic migrations.
9. Review cookie/token storage for the chosen frontend architecture.
