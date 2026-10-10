# API pagination

Collection endpoints use bounded pagination to keep responses predictable.
Clients should provide `limit` and `offset` when walking a large collection,
and should always use the response's ordering rather than relying on database
default order.

For interactive exploration, the generated OpenAPI page documents the accepted
query parameters for each collection endpoint.
