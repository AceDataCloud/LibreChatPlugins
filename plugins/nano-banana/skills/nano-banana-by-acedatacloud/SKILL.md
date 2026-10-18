---
name: nano-banana-by-acedatacloud
description: Use Nano Banana via Ace Data Cloud for image requests and for retrieving an existing task. Applies when the user asks for nano banana, nanobanana; not an official Nano Banana integration.
---

Use the `nano-banana-by-acedatacloud` MCP connection. This integration is provided by Ace Data Cloud; it is independent of the service brand and LibreChat maintainers.

- First connect the user's own Ace account through the MCP OAuth dialog. Chat-model credentials are a separate connection; never ask for a token in chat or store it in prompts.
- Inspect the available tool schema rather than guessing parameters or substituting a different model/service. The existing server is the source of the API contract.
- For a new operation, show the selected service/model, inputs and current price from the user's account, and obtain the user's confirmation of the bounded spend. Then call `nanobanana_generate_image` once. Never infer generation permission from installation or sign-in.
- Save the returned task ID. For progress or a request concerning an existing task, call `nanobanana_get_task` with that same ID. Do not resubmit generation to poll, retry automatically, or change the service as a fallback.
- Report pending as pending. On terminal failure stop polling; on terminal success present the final returned media URLs. A preview URL, installed plugin or green connection does not prove final success or a unique bill.
- Preserve authentication, permission, balance, moderation and rate-limit errors. Do not disclose or request credential values. If the user asks only to connect or inspect tools, do not send a generation request.
