# Authentication request flow

1. Validate the request body and normalize the login identifier.
2. Load the user by normalized identifier.
3. Verify the supplied password against the stored password hash.
4. Create an access token containing the user identifier and role claims.
5. Apply authorization dependencies to protected endpoints.

Unknown users and incorrect passwords should produce the same public failure
response so the endpoint does not reveal which accounts exist.
