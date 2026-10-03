# Architecture

Nexora uses a simple layered structure:

- `routers`: HTTP/API concerns
- `schemas`: request and response validation
- `models`: database entities
- `services`: business logic
- `security`: authentication and authorization
- `middleware`: cross-cutting HTTP behavior
- `scripts`: operational utilities

A sale is intentionally handled by a service instead of placing the complete workflow in a route. This keeps stock changes, sale creation and audit logging in one transaction.
