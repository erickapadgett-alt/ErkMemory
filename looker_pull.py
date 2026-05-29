#!/usr/bin/env python3
"""
Pull data from the VIP Medical Group Looker instance.

Setup:
    pip install looker-sdk
    # Credentials are read from (in order):
    #   1. looker.ini in this directory (gitignored), or
    #   2. LOOKERSDK_* environment variables

Usage:
    python looker_pull.py                 # smoke test: who am I + list models
    python looker_pull.py looks           # list saved Looks
    python looker_pull.py run-look 123    # run Look 123, print CSV
    python looker_pull.py dashboards      # list dashboards

NOTE: requires network egress to vipmedicalgroup.cloud.looker.com:19999.
If you see connection/allowlist errors, the host/port must be added to the
environment's network policy first (see knowledge/looker-api.md).
"""
import sys
import os

try:
    import looker_sdk
    from looker_sdk import models40 as models
except ImportError:
    sys.exit("Missing dependency. Run: pip install looker-sdk")


def get_sdk():
    # Prefer looker.ini if present, else fall back to env vars.
    ini = os.path.join(os.path.dirname(__file__), "looker.ini")
    if os.path.exists(ini):
        return looker_sdk.init40(config_file=ini)
    return looker_sdk.init40()


def main():
    sdk = get_sdk()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "whoami"

    if cmd == "whoami":
        me = sdk.me()
        print(f"Authenticated as: {me.display_name} <{me.email}> (id={me.id})")
        print("LookML models:", [m.name for m in sdk.all_lookml_models()][:25])

    elif cmd == "looks":
        for look in sdk.all_looks(fields="id,title"):
            print(f"{look.id}\t{look.title}")

    elif cmd == "dashboards":
        for d in sdk.all_dashboards(fields="id,title"):
            print(f"{d.id}\t{d.title}")

    elif cmd == "run-look" and len(sys.argv) > 2:
        look_id = sys.argv[2]
        print(sdk.run_look(look_id=look_id, result_format="csv"))

    else:
        sys.exit("Unknown command. See docstring for usage.")


if __name__ == "__main__":
    main()
