"""rn-ax fork additions on top of custom-components/healthchecksio.

Kept in its own module rather than inlined into the upstream files so a
future `git merge upstream/main` only has to reconcile the (few) call sites
in config_flow.py/coordinator.py, not logic living inside them. See
FORK.md for what's changed and why.
"""

from __future__ import annotations

from collections import OrderedDict

import voluptuous as vol


def build_user_data_schema(
    *, name: str, api_key: str, check: str, self_hosted: bool
) -> vol.Schema:
    """Schema for the user step.

    Adds a required `name` field (used as the config entry's title, since
    `check` -- upstream's title source -- is no longer always present) and
    makes `check` optional, so a project entry that exists purely to expose
    sensors doesn't need to also self-report a liveness ping.
    """
    data_schema = OrderedDict()
    data_schema[vol.Required("name", default=name)] = str
    data_schema[vol.Required("api_key", default=api_key)] = str
    data_schema[vol.Optional("check", default=check)] = str
    data_schema[vol.Required("self_hosted", default=self_hosted)] = bool
    return vol.Schema(data_schema)


def ping_url(
    *,
    check: str | None,
    self_hosted: bool,
    site_root: str,
    ping_endpoint: str | None,
) -> str | None:
    """URL to ping for this check, or None if no check is configured.

    A project entry added only to expose sensors (not to report this Home
    Assistant instance's own liveness) has no check to ping at all.
    """
    if not check:
        return None
    if self_hosted:
        return f"{site_root}/{ping_endpoint}/{check}"
    return f"https://hc-ping.com/{check}"
