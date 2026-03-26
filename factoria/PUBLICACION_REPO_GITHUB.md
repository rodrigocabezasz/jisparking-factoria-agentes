# Publicación y auditoría — [jisparking-factoria-agentes](https://github.com/rodrigocabezasz/jisparking-factoria-agentes)

## Hallazgos de auditoría (coherencia README ↔ archivos)

1. **`GUIA_OFICIAL_REG_TELEGRAM.md` en la raíz del repo**  
   El [README.md](../README.md) enlaza a **`factoria/GUIA_OFICIAL_REG_TELEGRAM.md`**. Si en GitHub la guía quedó solo en la raíz, los enlaces del README **rompen**.  
   **Acción:** mantener **una sola copia** en `factoria/GUIA_OFICIAL_REG_TELEGRAM.md` y **eliminar** `GUIA_OFICIAL_REG_TELEGRAM.md` de la raíz del repositorio.

2. **Documentos que el README cita y deben existir**

   - `factoria/GUIA_OFICIAL_REG_TELEGRAM.md`
   - `factoria/GOVERNANCE_STATE_ACTORS.md`
   - `factoria/openclaw-jislab-map.md`
   - `factoria/WEB_REG_Y_OPENCLAW.md`
   - `factoria/PASOS_ACTUALIZAR_OPENCLAW.md`
   - `factoria/INDICE_DOCUMENTACION.md` (opcional pero recomendado)
   - `factoria/PUBLICACION_REPO_GITHUB.md` (este archivo)
   - `factoria/openclaw.json.example`
   - `factoria/README_openclaw_json_example.md`
   - `factoria/workspace-asistente-jislab/SOUL.md` y `AGENTS.md`
   - `factoria/workspace-ops-despliegue-jislab/SOUL.md`
   - `scripts/export_dev_jis_to_github.py`
   - `scripts/factory_reg_post.py`
   - `.agents/Req_JIS/intake-message-schema.json`
   - `.agents/Req_JIS/dtr-template.md`

3. **Código de aplicación** (`main.py`, `apps/jis-intake`, Docker Compose completo)  
   Este repo oficial es **documentación + scripts + workspaces OpenClaw**. El runtime (intake, runner) vive en el monorepo de desarrollo / servidor JISLAB. No es obligatorio duplicarlo aquí salvo decisión explícita del equipo.

4. **`jis-reg-ui`**  
   Código en `apps/jis-reg-ui` del monorepo. Opcional: añadir un enlace en [WEB_REG_Y_OPENCLAW.md](WEB_REG_Y_OPENCLAW.md) al monorepo o subcarpeta `referencia/` con un README que apunte al código.

---

## Árbol mínimo recomendado en GitHub

```
README.md
factoria/
  GUIA_OFICIAL_REG_TELEGRAM.md
  GOVERNANCE_STATE_ACTORS.md
  openclaw-jislab-map.md
  WEB_REG_Y_OPENCLAW.md
  PASOS_ACTUALIZAR_OPENCLAW.md
  INDICE_DOCUMENTACION.md
  PUBLICACION_REPO_GITHUB.md
  openclaw.json.example
  README_openclaw_json_example.md
  workspace-asistente-jislab/
    SOUL.md
    AGENTS.md
  workspace-ops-despliegue-jislab/
    SOUL.md
scripts/
  export_dev_jis_to_github.py
  factory_reg_post.py
  sync-jisparking-factoria-repo.ps1
.agents/
  Req_JIS/
    intake-message-schema.json
    dtr-template.md
```

(`.github/`, `plantillas/` y otros documentos que ya tengan pueden conservarse.)

---

## Sincronizar desde el monorepo local (Windows)

Desde `C:\Desarrollo - Agentes` (o la raíz donde esté el script):

```powershell
.\scripts\sync-jisparking-factoria-repo.ps1 -TargetRepoRoot "C:\ruta\al\clone\jisparking-factoria-agentes"
```

Luego en el clon:

```powershell
cd C:\ruta\al\clone\jisparking-factoria-agentes
git status
git add -A
git commit -m "docs: alinear documentación oficial factoría con monorepo"
git push origin main
```

El script copia los archivos del manifiesto y **borra** `GUIA_OFICIAL_REG_TELEGRAM.md` en la raíz del destino si existe (evita duplicado).

---

## Checklist antes de dar por cerrado “repo oficial”

- [ ] No hay `GUIA_OFICIAL_REG_TELEGRAM.md` en la **raíz** (solo bajo `factoria/`).
- [ ] Todos los enlaces del README abren sin 404.
- [ ] `scripts/export_dev_jis_to_github.py` y `factory_reg_post.py` están presentes.
- [ ] `.agents/Req_JIS/` con schema y plantilla DTR.
- [ ] `openclaw.json.example` sin tokens reales.
