# Bugbot Review Guidelines — Microblog

 

## Security

- Never commit secrets, API keys, passwords, or tokens. Use environment variables.

- All SQL queries must use SQLAlchemy ORM or parameterized queries. Never concatenate or f-string user input into SQL.

- Never pass untrusted user input to `os.system`, `subprocess` with `shell=True`, `eval`, or `exec`.

 

## Reliability

- Handle the case where a database query returns no result before accessing fields.

- Validate and sanitize all user input from `request.args`, `request.form`, and URL parameters.

 

## Style

- Prefer `logging` over `print` for diagnostics.

- Use type hints on public functions.
