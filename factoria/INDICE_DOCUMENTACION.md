# Índice — Documentación factoría (repo oficial)

Punto de entrada para navegar la documentación en [jisparking-factoria-agentes](https://github.com/rodrigocabezasz/jisparking-factoria-agentes).

| Documento | Para qué sirve |
|-----------|----------------|
| [README.md](../README.md) | Flujo end-to-end, estados, GitHub, agentes, export a jislab-runtime. |
| [GUIA_OFICIAL_REG_TELEGRAM.md](GUIA_OFICIAL_REG_TELEGRAM.md) | Cómo redactar `/reg` en Telegram (oficial). |
| [GOVERNANCE_STATE_ACTORS.md](GOVERNANCE_STATE_ACTORS.md) | Dev_JIS, cola, auto-encolado, Kanban. |
| [openclaw-jislab-map.md](openclaw-jislab-map.md) | Dónde vive `openclaw.json` y enlaces útiles. |
| [WEB_REG_Y_OPENCLAW.md](WEB_REG_Y_OPENCLAW.md) | `jis-reg-ui`, chat web, actualización OpenClaw. |
| [PASOS_ACTUALIZAR_OPENCLAW.md](PASOS_ACTUALIZAR_OPENCLAW.md) | Checklist Docker para quitar aviso de versión. |
| [PUBLICACION_REPO_GITHUB.md](PUBLICACION_REPO_GITHUB.md) | Auditoría, qué subir, script de sincronización. |
| [openclaw.json.example](openclaw.json.example) | Plantilla de config sin secretos. |
| [README_openclaw_json_example.md](README_openclaw_json_example.md) | Cómo aplicar el ejemplo en el servidor. |
| [workspace-asistente-jislab/SOUL.md](workspace-asistente-jislab/SOUL.md) | Reglas del agente por defecto (`/reg`, exec). |
| [workspace-asistente-jislab/AGENTS.md](workspace-asistente-jislab/AGENTS.md) | Reglas cortas del mismo workspace. |
| [workspace-ops-despliegue-jislab/SOUL.md](workspace-ops-despliegue-jislab/SOUL.md) | Export sandbox → GitHub. |

## Contrato / intake

| Recurso | Uso |
|---------|-----|
| [../.agents/Req_JIS/intake-message-schema.json](../.agents/Req_JIS/intake-message-schema.json) | Schema JSON del payload completo. |
| [../.agents/Req_JIS/dtr-template.md](../.agents/Req_JIS/dtr-template.md) | Plantilla DTR (referencia). |

## Scripts (en `scripts/`)

| Script | Uso |
|--------|-----|
| [export_dev_jis_to_github.py](../scripts/export_dev_jis_to_github.py) | Push de `src/` y `tests/` del sandbox a rama `factoria/<REQ>`. |
| [factory_reg_post.py](../scripts/factory_reg_post.py) | POST a `/telegram/reg` desde el gateway (stdin o `--file`). |

## Documentos históricos / operación (opcional)

En la misma carpeta `factoria/` del monorepo pueden existir otros `.md` (auditorías, planes). No son obligatorios en el repo mínimo oficial; añadilos si el equipo los usa.
