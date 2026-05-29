# Looker API — VIP Medical Group

Reference for working with the VIP Medical Group Looker instance across all
Claude Code sessions.

> ⚠️ **The client secret is NOT stored in this repo.** It lives in a
> gitignored `looker.ini` (local to a session) and/or `LOOKERSDK_*`
> environment variables configured in the environment settings. Never commit
> the secret — git history is permanent.

## Connection details

| Item | Value |
|------|-------|
| Web UI | https://vipmedicalgroup.cloud.looker.com/ |
| API base URL | `https://vipmedicalgroup.cloud.looker.com:19999` |
| API version | `4.0` (current) |
| Auth | OAuth2 client credentials ("API Key for LookML") |
| Client ID | `bNBcwMGhg5sWgGD5Nqty` |
| Client Secret | **not stored here** — see `looker.ini` / env vars |

## Where credentials live

**This session (already set up):** a gitignored `looker.ini` at the repo root
holds the full credentials and is read automatically by the SDK and the
`looker_pull.py` helper.

**For persistence across sessions:** because each web session is a fresh
container (gitignored files and exported env vars do NOT carry over), set
these as **environment variables in the environment configuration**
(persisted, not in git):

```
LOOKERSDK_BASE_URL=https://vipmedicalgroup.cloud.looker.com:19999
LOOKERSDK_CLIENT_ID=bNBcwMGhg5sWgGD5Nqty
LOOKERSDK_CLIENT_SECRET=<client_secret>
LOOKERSDK_VERIFY_SSL=true
```

See: https://code.claude.com/docs/en/claude-code-on-the-web (env vars).

## ⚠️ Network access requirement

Pulling data requires outbound network egress to the Looker host **and the API
port 19999**. As of last test the environment's network policy blocked this:

- `vipmedicalgroup.cloud.looker.com` → **403 "Host not in allowlist"**
- port `:19999` → connection refused/blocked

**To enable data pulls:** add `vipmedicalgroup.cloud.looker.com` (and allow
port 19999) to the environment's network policy / allowlist. Reference:
https://code.claude.com/docs/en/claude-code-on-the-web (network policy).

## Pull data — helper script

`looker_pull.py` (repo root) wraps the common operations:

```bash
pip install looker-sdk
python looker_pull.py             # smoke test: whoami + list LookML models
python looker_pull.py looks       # list saved Looks (id + title)
python looker_pull.py dashboards  # list dashboards
python looker_pull.py run-look 42 # run Look 42, output CSV
```

## Auth flow (raw REST)

```bash
TOKEN=$(curl -s -X POST \
  "https://vipmedicalgroup.cloud.looker.com:19999/api/4.0/login" \
  -d "client_id=$LOOKERSDK_CLIENT_ID&client_secret=$LOOKERSDK_CLIENT_SECRET" \
  | jq -r .access_token)

curl -s "https://vipmedicalgroup.cloud.looker.com:19999/api/4.0/user" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## Python SDK

```python
import looker_sdk
sdk = looker_sdk.init40(config_file="looker.ini")   # or init40() for env vars
print(sdk.me())
looks = sdk.all_looks(fields="id,title")
csv = sdk.run_look(look_id="42", result_format="csv")
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

- API runs on port **:19999** (separate from the web UI on :443).
- Access tokens are short-lived (~1h); the SDK auto-refreshes. For raw curl,
  re-login on a 401.
- Rate limits apply per instance — batch where possible.
- Never paste the client secret into committed files, logs, or PRs.

## Status

- [x] Instance URL + client ID recorded
- [x] Local `looker.ini` created (gitignored) with full credentials
- [x] `looker_pull.py` helper ready
- [ ] **Add Looker host + port 19999 to environment network allowlist** (blocker)
- [ ] Set `LOOKERSDK_*` env vars in environment config for cross-session persistence
- [ ] Verify live pull: `python looker_pull.py`
