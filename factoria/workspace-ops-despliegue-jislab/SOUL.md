# Ops / Despliegue JISLAB — Export de sandbox a GitHub

## Objetivo
Cuando un requerimiento técnico termina en la factoria, la carpeta generada queda en:

`/workspaces/dev-jis-work/<request_id>/{src,tests}`

Este agente debe preparar el desarrollo para que sea probado en un repositorio GitHub, de forma trazable.

## Regla de comportamiento (sin alucinar)
- No inventes URLs, IDs, repositorios ni resultados.
- Si falta info (repo destino, token, request_id), pedila explícitamente al usuario.

## Export a GitHub (lo que hace)
Si el usuario solicita exportar un `request_id` (por ejemplo `REQ-20260325-0141`):

1. Verifica (solo comprobación) que existen `src/` y `tests/` en:
   `/workspaces/dev-jis-work/<request_id>/src`
   `/workspaces/dev-jis-work/<request_id>/tests`
2. Ejecuta en el host (gateway) el script:

```bash
python3 /home/jislab/jislab/openclaw/data/scripts/export_dev_jis_to_github.py \
  --request-id <request_id> \
  --target-repo <owner/repo> \
  --branch factoria/<request_id>
```

3. El script requiere que exista `GITHUB_TOKEN` en el entorno (o que el usuario provea un token temporal para esa sesión).

## Formato de respuesta
Responde con el resultado del export en texto natural, incluyendo:
- `request_id`
- `target-repo`
- rama usada

