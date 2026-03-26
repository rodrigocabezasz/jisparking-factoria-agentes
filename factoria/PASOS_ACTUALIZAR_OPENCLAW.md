# Pasos explícitos — Actualizar OpenClaw y quitar el aviso de versión

Este documento detalla el **punto operativo**: cómo actualizar la imagen/contenedor de OpenClaw en JISLAB y alinear `openclaw.json` para que la Control UI deje de mostrar el mensaje de actualización.

---

## Antes de empezar

- Tenés acceso **SSH** al servidor donde corre el contenedor `openclaw` (o el nombre real del contenedor).
- Conocés o podés recuperar el comando **`docker run`** o **`docker compose`** con el que se levantó OpenClaw (volúmenes y variables son críticos).

---

## Paso 1 — Ver qué imagen usás hoy

En el servidor:

```bash
docker ps --filter name=openclaw --format '{{.Names}}\t{{.Image}}'
docker inspect openclaw --format '{{.Config.Image}}'
```

Anotá **nombre de imagen** y **tag** (ej. `openclaw-openclaw:latest`).

---

## Paso 2 — Bajar la imagen nueva

```bash
docker pull <IMAGEN>:<TAG>
```

Ejemplo (ajustar a lo que salió en el Paso 1):

```bash
docker pull openclaw-openclaw:latest
```

Si no hay tag nuevo, el aviso puede seguir hasta que publiquen otra imagen.

---

## Paso 3 — Parar y eliminar el contenedor actual

```bash
docker stop openclaw
docker rm openclaw
```

(Si el contenedor tiene otro nombre, sustituí.)

---

## Paso 4 — Volver a crear el contenedor **igual que antes**

Ejecutá de nuevo el **`docker run`** (o `docker compose up -d`) que ya usaban, **sin cambiar**:

- montajes de volumen (`-v` …), sobre todo la carpeta de datos (`~/.openclaw` o la ruta que mapeéis);
- `--network host` u otra red, si aplica;
- puerto **18789** del gateway;
- variables de entorno (tokens, etc.).

Solo cambia que la imagen local ya está actualizada por el `docker pull`.

---

## Paso 5 — Alinear `meta` en `openclaw.json` (volumen de datos)

El aviso a veces compara la versión del binario con `meta.lastTouchedVersion` en el JSON que **lee el contenedor** (no solo el del repo Git).

1. Editá el `openclaw.json` dentro del volumen montado (en muchos despliegues: algo como `/home/jislab/jislab/openclaw/data/openclaw.json` o ruta equivalente en el host).

2. Ajustá el bloque (usá la versión que indique el changelog o la pantalla “About” de la nueva build):

```json
"meta": {
  "lastTouchedVersion": "2026.3.25",
  "lastTouchedAt": "2026-03-25T12:00:00.000Z"
}
```

3. Guardá el archivo.

---

## Paso 6 — Reiniciar OpenClaw (si no lo recreaste ya)

```bash
docker restart openclaw
```

---

## Paso 7 — Verificar

1. Abrí la Control UI (ej. `http://<host>:18789/chat?...`).
2. **Refrescá fuerte** el navegador (Ctrl+F5).
3. Comprobá si desapareció el banner de actualización.

Comando útil:

```bash
docker ps --filter name=openclaw
```

La columna `CREATED` debería ser reciente tras el redeploy.

---

## Si el aviso no desaparece

| Situación | Qué hacer |
|-----------|-----------|
| Sigue saliendo una versión **más nueva** que tu imagen | Hace falta esperar otra imagen o usar el tag que recomiende el proyecto OpenClaw. |
| Editaste JSON en el repo pero **no** en el volumen montado | Corregí el archivo que **realmente** monta el contenedor. |
| Contenedor viejo aún en ejecución | `docker ps -a` y asegurate de que solo quede el contenedor nuevo. |

---

## Referencia ampliada

Ver también [WEB_REG_Y_OPENCLAW.md](WEB_REG_Y_OPENCLAW.md) (sección 3).
