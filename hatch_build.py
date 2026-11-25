"""
Build hook that supplies client_secret.json to the distribution.

The credential is deliberately not in the repo: GitHub push protection
rejects Google OAuth secrets, and publicly scanned ones get reported to
Google and revoked. But it must ship inside the package so that a plain
`pip install pytubekit` works with no user setup.

So the build copies it in from outside the tree, trying in order:

  1. src/pytubekit/client_secret.json  -- already in place, left alone
  2. $PYTUBEKIT_CLIENT_SECRET  -- for release automation (CI secret -> file)
  3. `pass show gcp/veltzer-pytubekit-id/oauth-client`  -- the developer's password
     store, where every GCP credential lives (written out to the file in 1)

If none is found the build fails loudly. Without that, hatchling would
silently omit the file and produce a package that breaks on first run for
every user.
"""

import os
import shutil
import subprocess
from typing import override

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

CLIENT_SECRET = os.path.join("src", "pytubekit", "client_secret.json")
PASS_ENTRY = "gcp/veltzer-pytubekit-id/oauth-client"


def _pass_show(entry: str) -> str | None:
    """ the content of a pass(1) entry, or None when pass or the entry is missing """
    try:
        result = subprocess.run(["pass", "show", entry], capture_output=True, text=True, check=False)
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout


class CustomBuildHook(BuildHookInterface):
    @override
    def initialize(self, version, build_data):
        target = os.path.join(self.root, CLIENT_SECRET)
        if os.path.isfile(target):
            return

        source = os.environ.get("PYTUBEKIT_CLIENT_SECRET")
        if source and os.path.isfile(source):
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(source, target)
            build_data["artifacts"].append(f"/{CLIENT_SECRET}")
            self._copied = target
            return

        content = _pass_show(PASS_ENTRY)
        if content:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8") as stream:
                stream.write(content)
            build_data["artifacts"].append(f"/{CLIENT_SECRET}")
            self._copied = target
            return

        raise RuntimeError(
            f"missing {CLIENT_SECRET}\n"
            f"It is not kept in the repo. Store the credential in pass as "
            f"{PASS_ENTRY},\n"
            "or set PYTUBEKIT_CLIENT_SECRET to its path, before building."
        )

    @override
    def finalize(self, version, build_data, artifact_path):
        # The copy is not part of the source tree. Leaving it behind would make
        # the next build take the "already in place" branch above and silently
        # ship this stale copy instead of re-reading the real credential.
        copied = getattr(self, "_copied", None)
        if copied and os.path.isfile(copied):
            os.remove(copied)
            self._copied = None
