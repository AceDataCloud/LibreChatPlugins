# Ace Data Cloud service plugins for LibreChat

Five independently installable native **Agent Plugins 1.0.0**: **Suno**, **Seedance**, **HappyHorse**, **GPT Image**, and **Nano Banana**, each provided by **Ace Data Cloud**. Each package adds its own searchable Skill and hosted MCP connection using the existing Ace service implementation. These are independent integrations, not official plugins from the service brands or LibreChat maintainers.

[中文图文教程](readme/README_zh_Hans.md) · [Current API prices](https://platform.acedata.cloud/models?utm_source=librechat&utm_medium=referral&utm_campaign=evergreen&utm_content=plugins_readme_pricing)

## 1. Install one service

The [official LibreChat Agent Plugins guide](https://www.librechat.ai/docs/features/agent_plugins) describes this experimental package format. This repository is the package source; **it is not an official global marketplace listing**. The administrator installs the services the instance should expose. Ordinary users can then find them in that instance's MCP/Skills tool catalog.

| Service | Independent package | Existing MCP source |
| --- | --- | --- |
| [Suno by Ace Data Cloud](plugins/suno) | `suno-by-acedatacloud` | [SunoMCP](https://github.com/AceDataCloud/SunoMCP) |
| [Seedance by Ace Data Cloud](plugins/seedance) | `seedance-by-acedatacloud` | [SeedanceMCP](https://github.com/AceDataCloud/SeedanceMCP) |
| [HappyHorse by Ace Data Cloud](plugins/happyhorse) | `happyhorse-by-acedatacloud` | [HappyHorseMCP](https://github.com/AceDataCloud/HappyHorseMCP) |
| [GPT Image by Ace Data Cloud](plugins/gpt-image) | `gpt-image-by-acedatacloud` | [OpenAIMCP](https://github.com/AceDataCloud/OpenAIMCP) |
| [Nano Banana by Ace Data Cloud](plugins/nano-banana) | `nano-banana-by-acedatacloud` | [NanoBananaMCP](https://github.com/AceDataCloud/NanoBananaMCP) |

From a reviewed checkout of this repository, install **one** package to the LibreChat filesystem:

```bash
git clone https://github.com/AceDataCloud/LibreChatPlugins.git
cd LibreChatPlugins
python3 scripts/install.py suno --plugin-dir /path/to/LibreChat/plugin
```

Replace `suno` with another service slug to install it separately. The installer refuses to overwrite an existing package. For Docker, the chosen plugin directory must be visible at `/app/plugin` (merge a read-only volume into your existing override; retain all existing mounts). LibreChat loads each immediate child at startup. Restart that instance after installation. No hooks, shell commands or embedded credentials are included in a package. `DEPLOYMENT_PLUGINS_DIR` can select another operator-controlled directory.

This requires a LibreChat version implementing [Agent Plugins](https://www.librechat.ai/docs/features/agent_plugins); the format is experimental. A successful archive copy does not prove the current released host supports it. Upstream parser validation and runtime installation are separate evidence.

## 2. Register/sign in and check service access

Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=librechat&utm_medium=referral&utm_campaign=evergreen&utm_content=plugins_readme_api_key). Register or sign in. Find **General application**; if absent, choose **Initialize General Application**. Review the selected service, current prices and balance. A General key accesses services your account is entitled to use; a service-specific key is limited to that service.

To copy a key, use the application card. To create a separately revocable LibreChat key, use **Keys / Manage Keys → Create**. Check expiration, usage limit and allowed APIs, including both generation and task lookup for an asynchronous service.

![Copy an API key or open Manage Keys](assets/tutorial/get-api-key-en.png)

![Create a dedicated key with optional restrictions](assets/tutorial/create-api-key-en.png)

These real Ace Console screenshots are reused from the Dify onboarding guide, pinned in [image sources](assets/tutorial/source.json). Keys are redacted. Account trial credit is whatever your current account displays; installation does not include a credit grant.

## 3. Connect the service inside LibreChat

**Native plugin route (OAuth):** Open the installed service's MCP entry in the chat input's **+ → MCP Servers** menu or **MCP Settings**, then choose its connection/sign-in action. Complete the Ace account login/consent in the same browser session. The plugin contains only its HTTPS URL; the host manages each user's OAuth connection. DCR registers the client; it is not a user API token. Actual sign-in and service calls must still be validated on the selected LibreChat version.

**Personal API Token route (separate optional configuration):** If OAuth cannot be used, an administrator may instead configure that MCP in `librechat.yaml` with a sensitive `customUserVars` Token field, as described in the [official MCP guide](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers). Paste the raw API Token into that service's MCP field; do not add `Bearer ` in the field. Do not paste a management `platform-...` token, the Token into chat, or a key into shared plugin files. A YAML server with the same name takes precedence over a plugin server. Do not configure both OAuth and a fixed header for one connection.

![Personal MCP Token dialog preview, not an actual run](assets/tutorial/librechat-suno-token-preview.png)

**Official-screenshot edit, 2026-10-17; not an actual Ace run.** This image explains the optional personal MCP Token route, not the OAuth sign-in or chat-model key dialog. Chat model credentials are entered separately after choosing the chat endpoint. Original screenshot capture date/version are not established; [source and limits](assets/tutorial/source.json).

## 4. First use and the same task ID

First confirm the service appears and the authenticated connection lists tools. This is an installation check, not generation success or a balance check. A static model/action guide only proves tool loading.

For a free read-only check, use an existing successful task that belongs to your account. Ask the service to retrieve **that same ID**, or use a direct tool test if the host provides one. A chat model may itself incur costs; do not send a model-driven request merely to perform a free connection check.

For a new generation, first choose the service/model and inputs, check current price and obtain a bounded spend confirmation. Submit once, retain the returned task ID and query it until terminal success or failure. Do not rerun generation to poll. Pending previews are not final media. Stop after terminal failure. Verify final media and the corresponding unique bill separately. No new paid generation was performed to publish these packages.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Service missing | Host supports Agent Plugins; package is an immediate child under the mounted plugin directory; restart and inspect manifest diagnostics. |
| OAuth cannot connect | Keep one auth route, use the same browser session, check service URL and public OAuth metadata. Do not insert a guessed Token or create duplicate identities. |
| 401 / 403 | Correct API token type, service/API permission, expiration, balance and moderation response. A visible tool does not prove permission for generation. |
| pending / empty media | Query the same task ID. Never submit a new generation just to check progress. |
| 429 / timeout / failure | Stop uncontrolled retries; inspect the existing task/error and service limits before any new paid request. |

The GPT Image package reuses the existing OpenAI MCP, which exposes additional OpenAI tools. Its branded Skill guides GPT Image requests; it does not limit the token's permissions. Restrict Allowed APIs to the operations needed. No model/service fallback is added.

## Validation and publication boundary

```bash
npm ci --ignore-scripts
npm run verify
python3 -m unittest discover -s tests
```

Verification checks native manifests/MCP configurations against the pinned upstream parser. It is not a LibreChat UI install or OAuth completion. Package source review, release files, official documentation acceptance, instance installation, authenticated tools, final media and billing are separate stages. No claimed downloads, users, ranking or revenue.

[Source issues](https://github.com/AceDataCloud/LibreChatPlugins/issues) · [Privacy](PRIVACY.md) · dev@acedata.cloud
