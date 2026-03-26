# Web `/reg` determinístico + actualización de OpenClaw

## 1) Por qué el chat web falla con `/reg`

La **Control UI** de OpenClaw manda el mensaje al **modelo** (Ollama). Ese modelo debe generar una llamada `exec` perfecta; a menudo **no** lo hace y solo muestra JSON incompleto. **Telegram** y los scripts llaman al **intake por HTTP** sin depender del modelo.

**Solución en este repo:** servicio **`jis-reg-ui`** — formulario HTML que hace `POST` directo a `http://127.0.0.1:8089/telegram/reg` (misma ruta que `factory_reg_post.py`).

## 2) Desplegar `jis-reg-ui` en JISLAB

Desde la carpeta del repo (o copiando `apps/jis-reg-ui` al servidor):

```bash
cd apps/jis-reg-ui
docker build -t jis-reg-ui:latest .
docker run -d --name jis-reg-ui --restart unless-stopped \
  --network host \
  -e JIS_INTAKE_TELEGRAM_REG=http://127.0.0.1:8089/telegram/reg \
  jis-reg-ui:latest
```

- **`--network host`:** el contenedor ve `127.0.0.1:8089` donde corre `jis-intake`. Si usás bridge, cambiá la URL del intake por el nombre del servicio Docker.

Probar:

```bash
curl -sS http://127.0.0.1:8095/health
```

Abrir en el navegador: `http://<IP-o-dominio>:8095/` (abrir **8095** en firewall / reverse proxy si hace falta).

Opcional: detrás de Nginx con TLS y Basic Auth; no exponer sin protección en Internet.

## 3) Quitar el aviso de “actualización disponible” en OpenClaw

**Checklist paso a paso (copiar en servidor):** [PASOS_ACTUALIZAR_OPENCLAW.md](PASOS_ACTUALIZAR_OPENCLAW.md).

Ese mensaje aparece cuando la **versión del programa** dentro del contenedor es **menor** que la que la UI considera actual (suele leerse de `openclaw.json` → `meta.lastTouchedVersion` o equivalente interno).

### 3.1 Pasos recomendados (JISLAB)

1. **Anotar** cómo levantan OpenClaw hoy (imagen, `docker run` o compose, volúmenes).  
   Ejemplo de inspección:

   ```bash
   docker inspect openclaw --format '{{.Config.Image}}'
   ```

2. **Actualizar la imagen** al mismo tag que usan (muchas veces `latest`):

   ```bash
   docker pull <IMAGEN_QUE_SALIO_EN_INSPECT>:<TAG>
   ```

3. **Recrear el contenedor** con el **mismo** comando que ya tenían (mismos `-v`, `-e`, `--network`, puerto **18789**, etc.). Solo cambia que ahora la capa local está al día.

   ```bash
   docker stop openclaw && docker rm openclaw
   # ... tu docker run completo ...
   ```

4. **Alinear `openclaw.json` en el volumen de datos** del gateway (en muchos despliegues: carpeta montada en `/home/node/.openclaw` o ruta equivalente). Copiá desde el repo el `openclaw.json` actualizado o editá a mano el bloque:

   ```json
   "meta": {
     "lastTouchedVersion": "2026.3.25",
     "lastTouchedAt": "2026-03-25T12:00:00.000Z"
   }
   ```

   Usá la **versión que indique la documentación o el changelog** de la imagen que acaban de pullear (si publican semver tipo `2026.3.25`, que coincida con `lastTouchedVersion`).

5. **Reiniciar** OpenClaw y **refrescar** la Control UI con Ctrl+F5.

### 3.2 Si el aviso sigue

- Confirmar que el contenedor en ejecución es el nuevo: `docker ps` → `CREATED` reciente.
- Revisar que el `openclaw.json` **montado** sea el que editaste (a veces hay copia en disco distinta a la del repo).
- Si la UI compara contra un canal de actualizaciones online, puede haber una versión **aún más nueva** que la imagen publicada: en ese caso hace falta **otro** `docker pull` cuando salga la imagen correspondiente.

### 3.3 Seguridad

**No** subas tokens al repositorio: `gateway.auth.token` y tokens de Telegram deben vivir solo en el servidor o en secretos.

## 4) ¿Se puede integrar `/reg` *dentro* del chat web sin página aparte?

Solo si la **versión de OpenClaw** que usan expone algo equivalente a `channels.telegram.customCommands` para **web** o un **hook previo al modelo** (depende del producto). Este repo no incluye el código fuente de OpenClaw; la alternativa portable es **`jis-reg-ui`** o seguir con **Telegram**.

## 5) Resumen

| Canal | Comportamiento |
|--------|----------------|
| Telegram bot | HTTP directo al intake → estable |
| `jis-reg-ui` | Mismo POST que `/telegram/reg` → estable |
| WebChat OpenClaw | Depende del modelo → a veces JSON roto |
