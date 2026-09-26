"""Adds config flow for Blueprint."""

from __future__ import annotations

import asyncio
import json
from collections import OrderedDict
from logging import getLogger

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import _fork
from .const import DOMAIN, OFFICIAL_SITE_ROOT

LOGGER = getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class BlueprintFlowHandler(config_entries.ConfigFlow):
    """Config flow for Blueprint."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self.initial_data = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            if user_input["self_hosted"]:
                # don't check yet, we need more info
                self.initial_data = user_input
                return await self._show_self_hosted_config_flow(user_input)
            else:
                valid = await self._test_credentials(
                    user_input["api_key"],
                    user_input.get("check"),
                    False,
                    OFFICIAL_SITE_ROOT,
                    None,
                )
                if valid:
                    user_input["self_hosted"] = False
                    return self.async_create_entry(
                        title=user_input["name"], data=user_input
                    )
                else:
                    self._errors["base"] = "auth"

        return await self._show_initial_config_form(user_input)

    async def _show_initial_config_form(self, user_input):
        """Show the configuration form to edit check data."""
        # Defaults
        name = ""
        api_key = ""
        check = ""
        self_hosted = False

        if user_input is not None:
            if "name" in user_input:
                name = user_input["name"]
            if "api_key" in user_input:
                api_key = user_input["api_key"]
            if "check" in user_input:
                check = user_input["check"]
            if "self_hosted" in user_input:
                self_hosted = user_input["self_hosted"]

        data_schema = _fork.build_user_data_schema(
            name=name, api_key=api_key, check=check, self_hosted=self_hosted
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=self._errors,
            description_placeholders={"docs_url": _fork.DOCS_URL},
        )

    async def async_step_self_hosted(self, user_input):
        """Handle the step for a self-hosted instance."""
        self._errors = {}
        valid = await self._test_credentials(
            self.initial_data["api_key"],
            self.initial_data.get("check"),
            True,
            user_input["site_root"],
            user_input["ping_endpoint"],
        )
        if valid:
            # merge data from initial config flow and this flow
            data = {**self.initial_data, **user_input}
            return self.async_create_entry(title=self.initial_data["name"], data=data)
        else:
            self._errors["base"] = "auth"

        return await self._show_self_hosted_config_flow(user_input)

    async def _show_self_hosted_config_flow(self, user_input):
        """Show the configuration form to edit self-hosted instance data."""
        # Defaults
        site_root = "https://checks.mydomain.com"
        ping_endpoint = "ping"

        if "site_root" in user_input:
            site_root = user_input["site_root"]
        if "ping_endpoint" in user_input:
            ping_endpoint = user_input["ping_endpoint"]

        data_schema = OrderedDict()
        data_schema[vol.Required("site_root", default=site_root)] = str
        data_schema[vol.Required("ping_endpoint", default=ping_endpoint)] = str
        return self.async_show_form(
            step_id="self_hosted",
            data_schema=vol.Schema(data_schema),
            errors=self._errors,
            description_placeholders={"docs_url": _fork.DOCS_URL},
        )

    async def _test_credentials(
        self, api_key, check, self_hosted, site_root, ping_endpoint
    ):
        """Return true if credentials is valid."""
        LOGGER.debug("Testing Credentials")
        verify_ssl = not self_hosted or site_root.startswith("https")
        session = async_get_clientsession(self.hass, verify_ssl)
        timeout10 = aiohttp.ClientTimeout(total=10)
        headers = {"X-Api-Key": api_key}
        check_url = _fork.ping_url(
            check=check,
            self_hosted=self_hosted,
            site_root=site_root,
            ping_endpoint=ping_endpoint,
        )
        if check_url:
            await asyncio.sleep(1)  # needed for self-hosted instances
            try:
                check_response = await session.get(check_url, timeout=timeout10)
            except (TimeoutError, aiohttp.ClientError):
                LOGGER.exception("Could Not Send Check")
                return False
            else:
                if check_response.ok:
                    LOGGER.debug(
                        "Send Check HTTP Status Code: %s", check_response.status
                    )
                else:
                    LOGGER.error(
                        "Send Check HTTP Status Code: %s", check_response.status
                    )
                    return False
        try:
            request = await session.get(
                f"{site_root}/api/v1/checks/", headers=headers, timeout=timeout10
            )
        except (TimeoutError, aiohttp.ClientError):
            LOGGER.exception("Could Not Update Data")
            return False
        except (ValueError, json.decoder.JSONDecodeError):
            LOGGER.exception("Data JSON Decode Error")
            return False
        else:
            if not request.ok:
                LOGGER.error("Got Data HTTP Status Code: %s", request.status)
                return False
            LOGGER.debug("Got Data HTTP Status Code: %s", request.status)
            return True
