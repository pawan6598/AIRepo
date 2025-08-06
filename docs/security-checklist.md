# Security Audit Checklist

- [ ] Dependency vulnerability scan (e.g., `pip audit`, `npm audit`).
- [ ] Secrets stored in `.env` and never committed.
- [ ] JWT secrets rotated regularly.
- [ ] HTTPS enforced in production.
- [ ] Ports exposed only as necessary in Docker.
- [ ] RBAC for database and cloud resources.
