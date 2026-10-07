# Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Account enumeration | Use one generic invalid-credentials response. |
| Long-lived stolen token | Keep access tokens short-lived and plan revocation. |
| Privilege escalation | Resolve roles server-side and test every dependency. |
| Secret leakage | Exclude sensitive fields from logs, errors, and schemas. |

The first implementation should favor a small, testable authentication surface
over adding refresh-token complexity before the access-token path is stable.
