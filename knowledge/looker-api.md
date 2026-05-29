# Looker API

Reference for working with the Looker API across all Claude Code sessions.

> ⚠️ **Secrets are NOT stored in this repo.** Following the convention in
> `knowledge/systems.md`, the actual client ID / secret live in the
> credentials store (`~/.config/clawdbot/credentials`) and/or environment
> variables. This file documents *how* to use the API and *where* the
> credentials are expected — not the secret values themselves.

## Credentials (fill in / confirm)

Provided in a prior chat — values must be placed in the credentials store or
exported as env vars before use. **Placeholders below — replace `<...>`:**

| Item | Env var | Value |
|------|---------|-------|
| Instance / API base URL | `LOOKERSDK_BASE_URL` | `https://<instance>.cloud.looker.com:19999` |
| Client ID | `LOOKERSDK_CLIENT_ID` | `<client_id>` |
| Client secret | `LOOKERSDK_CLIENT_SECRET` | `<client_secret>` (secret — store securely) |
| Verify SSL | `LOOKERSDK_VERIFY_SSL` | `true` |
| API version | — | `4.0` (current) |

Store secrets one of these ways:

```bash
# Option A: export env vars (e.g. in shell profile or session-env)
export LOOKERSDK_BASE_URL="https://<instance>.cloud.looker.com:19999"
export LOOKERSDK_CLIENT_ID="<client_id>"
export LOOKERSDK_CLIENT_SECRET="<client_secret>"
export LOOKERSDK_VERIFY_SSL=true
```

```ini
# Option B: looker.ini (gitignored — never commit)
[Looker]
base_url=https://<instance>.cloud.looker.com:19999
client_id=<client_id>
client_secret=<client_secret>
verify_ssl=true
timeout=120
```

## Auth flow (raw REST)

The API uses OAuth2 client-credentials. Exchange the client ID/secret for a
short-lived access token, then send it as a Bearer token.

```bash
# 1. Get an access token
TOKEN=$(curl -s -X POST \
  "$LOOKERSDK_BASE_URL/api/4.0/login" \
  -d "client_id=$LOOKERSDK_CLIENT_ID&client_secret=$LOOKERSDK_CLIENT_SECRET" \
  | jq -r .access_token)

# 2. Call an endpoint
curl -s "$LOOKERSDK_BASE_URL/api/4.0/user" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## Python SDK (recommended)

```bash
pip install looker-sdk
```

```python
import looker_sdk

# Reads LOOKERSDK_* env vars or looker.ini automatically
sdk = looker_sdk.init40()          # API 4.0

me = sdk.me()                      # current user
looks = sdk.all_looks()            # list saved Looks
# Run a query / inline query, get results as CSV/JSON, etc.
```

## Common endpoints (API 4.0)

| Purpose | Endpoint |
|---------|----------|
| Login (get token) | `POST /api/4.0/login` |
| Current user | `GET /api/4.0/user` |
| List dashboards | `GET /api/4.0/dashboards` |
| List Looks | `GET /api/4.0/looks` |
| Run a Look | `GET /api/4.0/looks/{look_id}/run/{format}` (json/csv/png…) |
| Run inline query | `POST /api/4.0/queries/run/{format}` |
| List LookML models | `GET /api/4.0/lookml_models` |

## Notes / gotchas

- API runs on port **:19999** by default (separate from the web UI on :443/:9999).
- Access tokens are short-lived (~1h); the SDK auto-refreshes. For raw curl,
  re-login when you get a 401.
- Rate limits apply per instance — batch where possible.
- Never paste the client secret into committed files, logs, or PRs.

## TODO / verify

- [ ] Confirm the real instance base URL (replace `<instance>`).
- [ ] Place client ID/secret into `~/.config/clawdbot/credentials` or env vars.
- [ ] Test auth with the curl login snippet above.
