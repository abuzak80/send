import ssl

import httpx

httpx_ssl_context = httpx.create_ssl_context(
    verify=ssl.create_default_context(), trust_env=True
)
