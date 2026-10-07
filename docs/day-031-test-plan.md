# Authentication test plan

The implementation should cover:

- valid credentials return a token;
- an unknown account is rejected;
- an incorrect password is rejected;
- expired and malformed tokens are rejected;
- a valid token identifies the expected user;
- role-protected routes deny insufficient roles;
- authentication failures create safe audit records;
- sensitive values never appear in logs or response bodies.
