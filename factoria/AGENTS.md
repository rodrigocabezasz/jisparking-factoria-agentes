# Asistente JISLAB

- Cumplí **SOUL.md**: respondé siempre al chat general; para `/reg` usá el script `factory_reg_post.py` (ver SOUL), sin `curl` ni puertos inventados.
- El agente tiene herramienta **exec** (`group:runtime`): si ves JSON de herramienta en el chat, suele faltar desplegar `openclaw.json` con `group:runtime` en `tools.allow`.

Si algo falla, reportá el error HTTP o el cuerpo JSON; no asumas éxito.
