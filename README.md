# healthchecksio

> [!IMPORTANT]
> **This is a fork of [custom-components/healthchecksio](https://github.com/custom-components/healthchecksio).** Why: Healthchecks.io scopes each API key to a single project, but upstream only allows one config entry ever, so an account with checks spread across multiple projects can only ever monitor one of them. Upstream tracks this as [#217](https://github.com/custom-components/healthchecksio/issues/217) (open since 2026-07-27, no maintainer engagement; an earlier duplicate, [#36](https://github.com/custom-components/healthchecksio/issues/36), was closed as "working as intended"). **Drop this fork and switch back to upstream if #217 ever lands.**
>
> Changes from upstream (kept isolated in [`custom_components/healthchecksio/_fork.py`](custom_components/healthchecksio/_fork.py) to minimize merge conflicts — update this list whenever that changes):
> - Removed the single-instance restriction, so each Healthchecks.io project can be added as its own config entry.
> - Made the "Check ID" field optional, so a project-only entry doesn't have to self-ping a check that isn't meant for Home Assistant.
> - Added a required "Project name" field, used as each entry's title (upstream used `check` for this, which is no longer always set).

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE.md)

[![hacs][hacsbadge]](hacs)
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Integration to integrate with [healthchecks.io][healthchecksio]._

![example][exampleimg]

## Installation

Search for and install `healthchecksio` from [HACS](https://hacs.xyz/)

## Configuration

This integration can **only** be configured via the UI. Add it once per Healthchecks.io project — each project has its own API key.

### Project name

A label for this project, used as the config entry's title so multiple entries (one per project) are distinguishable in Settings → Devices & Services.

### Check ID

Optional. The ID of a check that this Home Assistant instance should ping every 5 minutes to report its own liveness. Looks something like `aa247c51-8da8-4800-86a3-48763142e902`. Leave blank for a project entry that's only there to expose its checks as entities.

### What the integration does

- If a Check ID is set, pings that Healthchecks.io check every 5 minutes to monitor the state of Home Assistant.
- Pulls all of this project's Healthchecks.io checks as entities, so you can monitor their statuses directly in Home Assistant.

### API Key

The API key to your account. You can find it under the "Settings" tab in your project.

> [!NOTE]
> A **Full Access** API key is required for this integration to function correctly. This is because the integration both pings checks (which requires write access) and reads the status of all your checks to create entities in Home Assistant (which requires read access). Only the Full Access key provides both permissions needed for these operations.


## For self-hosted instances

### Site Root

This is the root URL of your Healthchecks.io instance.

### Ping Endpoint

This is the path of the endpoint used for pings.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Analytics

If you are using this integration, please consider enabling [Home Assistant usage analytics](https://www.home-assistant.io/integrations/analytics/#usage-analytics).

***

[healthchecksio]: https://healthchecks.io
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/healthchecksio.svg?style=for-the-badge
[commits]: https://github.com/custom-components/healthchecksio/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/healthchecksio.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40ludeeus-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/healthchecksio.svg?style=for-the-badge
[releases]: https://github.com/custom-components/healthchecksio/releases
