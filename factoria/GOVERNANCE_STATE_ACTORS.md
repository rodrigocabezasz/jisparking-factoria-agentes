# Gobierno de actores: PM-O vs Dev_JIS (decisión de implementación)

## Decisión (vigente en código)

1. **`POST /events/state-change`** es la API genérica de transición: cualquier cliente autenticado en el borde (OpenClaw UI, scripts, automation) puede enviar `actor` y `new_state`. No hay token distinto por rol en el payload; la confianza viene del despliegue (red privada, reverse proxy, futuro API key).

2. **Actor `Dev_JIS` tiene dos significados operativos**:
   - **Encolado de trabajo técnico**: un evento `state_changed` con `actor="Dev_JIS"` y `new_state="In Progress"` es lo que **consume** `GET /dev-jis/pending` en [main.py](../main.py) (cola del `factory-runner`). Sin ese evento, el worker no ve trabajo aunque el request exista en Backlog.
   - **Cierre técnico**: el proceso [apps/factory-runner/dev_jis_worker.py](../apps/factory-runner/dev_jis_worker.py) llama de nuevo a `POST /events/state-change` con `actor="Dev_JIS"` y `new_state` en `Done` o `Blocked` según pytest.

3. **PM-O (Jefe de Proyecto en OpenClaw)** es un **perfil de chat** para planificación humana o semi-automática. **No** es hoy el único actor autorizado en la API: el documento de “8 agentes” lo planteaba como orquestador exclusivo; en la implementación real el **runner técnico** usa `Dev_JIS` para avanzar estados de forma automática.

4. **Alineación con el documento de producto**: si se requiere que solo PM-O dispare transiciones, habría que añadir **autenticación por rol** (p. ej. header `X-Actor-Token`) y validar transiciones permitidas; eso queda como evolución. Mientras tanto, el modelo documentado aquí es el que refleja el código.

## Variable de entorno: `AUTO_ENQUEUE_DEV_JIS`

- Por defecto **`true`** en rutas **`POST /intake`**, `/telegram/reg`, `/simple-intake` y **`POST /telegram/webhook`**: tras `process_intake`, se aplica una transición automática a `In Progress` con `actor=Dev_JIS` para alimentar la cola del `factory-runner` sin paso manual. (Algunos bots publican solo en `/intake`; sin este paso quedaban en Backlog.)
- Con `AUTO_ENQUEUE_DEV_JIS=false`, el encolado debe hacerse explícitamente con `POST /events/state-change` (útil para CI o flujos solo Backlog).

## Trazabilidad en GitHub (Kanban)

- Cada `POST /events/state-change` con issue asociado puede dejar un **comentario** en el issue (`GITHUB_ISSUE_ON_STATE_CHANGE`, default activo) y sincronizar **labels** + campo **State** del Project v2 si está configurado.
- Las opciones del campo `State` en GitHub deben coincidir en nombre con los estados usados (`Backlog`, `In Progress`, `Done`, …); el intake hace matching flexible de mayúsculas/espacios.

## Referencias

- Cola pendiente: `GET /dev-jis/pending` filtra `event_type=state_changed`, `actor='Dev_JIS'`, `new_state='In Progress'`.
- Worker: [dev_jis_worker.py](../apps/factory-runner/dev_jis_worker.py).
- Evolución multi-rol (MySQL, opcional): [schema_8_agent_factory_tasks.sql](schema_8_agent_factory_tasks.sql).
