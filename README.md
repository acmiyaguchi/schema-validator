# mozschema-validator

A continuous integration service for Mozilla pipeline schemas.

# API

```
METHOD, ENDPOINT, USAGE, RETURNS
GET /v1/schemas/{id}
GET /v1/schemas
PUT /v1/validate?ids={ids}
GET /v1/summarize?id={id}
GET /v1/summarize/compare?base={id}?other={id}
```