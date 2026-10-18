# GPT Image by Ace Data Cloud for LibreChat

Independent native Agent Plugin for GPT Image image tools. Provided by **Ace Data Cloud**, not the GPT Image publisher or LibreChat maintainers.

[English installation and illustrated account setup](../../README.md) · [中文图文安装](../../readme/README_zh_Hans.md)

Install **only this service** with `python scripts/install.py gpt-image --plugin-dir /path/to/LibreChat/plugin` from a reviewed checkout of this repository. The plugin loads its own Skill and hosted OAuth MCP at LibreChat startup; no YAML editing or embedded API key is needed for this route. Restart the instance, then find `gpt-image-by-acedatacloud` in MCP tools or the service Skill by its name/description. This is an operator-installed package, not an entry in a global LibreChat marketplace.

Endpoint: `https://openai.mcp.acedata.cloud/mcp`. Existing implementation: https://github.com/AceDataCloud/OpenAIMCP (mcp-openai-pro); this package does not copy the worker or billing rules.

Use the MCP sign-in dialog to authorize your own Ace account. If using the separate manual-Token route in the main guide, paste only the raw personal API token in that service's MCP field; never the chat-model key dialog or a prompt. Review service access and current balance/pricing before a paid request.

First free check: connect and list tools. Optional read-only use: call `openai_get_task` with a successful task ID already belonging to your account. New `openai_generate_image` calls can be billed; submit once and retrieve the same ID until terminal success/failure. Final media and the unique bill require separate verification. The GPT Image package's existing MCP also exposes other OpenAI tools; its Skill guides GPT Image use but is not an authorization sandbox.

[Account and API key](https://platform.acedata.cloud/console/applications?utm_source=librechat&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image_plugin_api_key) · [Current pricing](https://platform.acedata.cloud/models?utm_source=librechat&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image_plugin_pricing)
