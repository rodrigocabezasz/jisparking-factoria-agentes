# Mapa OpenClaw: repositorio local vs JISLAB

## Rutas

| Ubicación | Ruta |
|-----------|------|
| Referencia en este repo | [openclaw.json](../openclaw.json) |
| Servidor JISLAB (típico) | `/home/jislab/jislab/openclaw/data/openclaw.json` |
| Web `/reg` sin LLM (opcional) | [WEB_REG_Y_OPENCLAW.md](WEB_REG_Y_OPENCLAW.md) — servicio `apps/jis-reg-ui` |
| Guía oficial texto `/reg` (Telegram) | [GUIA_OFICIAL_REG_TELEGRAM.md](GUIA_OFICIAL_REG_TELEGRAM.md) |
| Pasos actualizar OpenClaw (quitar aviso UI) | [PASOS_ACTUALIZAR_OPENCLAW.md](PASOS_ACTUALIZAR_OPENCLAW.md) |
| README flujo completo (GitHub raíz) | [../README.md](../README.md) |
| Índice documentación | [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md) |
| Publicación / auditoría GitHub | [PUBLICACION_REPO_GITHUB.md](PUBLICACION_REPO_GITHUB.md) |

## Cómo contrastar

Desde una máquina con acceso SSH a `jislab`:

```bash
ssh jislab cat /home/jislab/jislab/openclaw/data/openclaw.json > /tmp/openclaw-jislab.json
python scripts/compare_openclaw_configs.py openclaw.json /tmp/openclaw-jislab.json
```

El script lista `gateway.port`, `telegram.enabled`, `customCommands` (incl. `/reg`) y los nombres de cada entrada en `agents[]`, y muestra diferencias entre archivos.

## Snapshot local (generado desde el repo; actualizar si cambia openclaw.json)

Ejecutar: `python scripts/compare_openclaw_configs.py`

Salida de referencia (ejemplo):

- `gateway.port`: 18789
- `telegram.enabled`: false
- `customCommands`: comando `reg` con descripción "Registrar requerimiento en factoria"
- `agents[]`: Asistente JISLAB; Asistente JISLAB Skill; Arquitecto de Soluciones Técnicas; Jefe de Proyecto JISLAB; DBA MySQL; Desarrollador Backend JISPARKING; Frontend Specialist JISParking

Puntos a vigilar frente al servidor:

1. **Agentes**: el repo define perfiles (Asistente JISLAB, Arquitecto, Jefe de Proyecto, DBA, Backend, Frontend, etc.); el servidor debe alinear instrucciones de `/reg` con `POST` a `http://localhost:8089/telegram/reg` (o el host/puerto reales del intake en ese host).
2. **Telegram**: `channels.telegram.enabled` y `customCommands` para `/reg` deben coincidir con el despliegue (webhook vs agente).
3. **Gateway**: `gateway.port` (p. ej. 18789) y `auth.token` deben coincidir con cómo accedes a la Control UI.

## Acceso a la Control UI desde fuera de la LAN

Si `https://jisparking.from-vt.com:18789` no abre pero `http://192.168.0.22:18789` sí:

1. **DNS** debe apuntar al host que realmente expone el puerto (VPS, otra máquina con reverse proxy, o túnel).
2. **Firewall / router**: abrir o reenviar **18789** (o **443** si usás TLS delante) hasta el proceso del gateway.
3. **Reverse proxy** (Nginx/Caddy) en el borde: `proxy_pass` al `192.168.0.22:18789` solo si hay **ruta de red** desde el VPS hasta JISLAB (VPN, Tailscale, túnel SSH, etc.). Si el VPS no alcanza la LAN 192.168.x.x, hay que exponer el gateway por otro medio (p. ej. túnel Cloudflare, FRP, o mover OpenClaw al VPS).
4. En `openclaw.json`, `gateway.controlUi.allowedOrigins` debe incluir el origen del navegador (`https://jisparking.from-vt.com` con o sin puerto). Tras cambiar, reiniciar el contenedor `openclaw`.
5. `dangerouslyAllowHostHeaderOriginFallback: true` ayuda detrás de proxy cuando el `Host` no coincide con el origen; evaluar riesgo en entornos no confiables.

## Estado de verificación remota

En el entorno donde se ejecutó la implementación del plan, la conexión SSH a `jislab` no estaba disponible (*connection refused*). La comparación efectiva debe repetirse cuando la red/VPN permita acceso.
