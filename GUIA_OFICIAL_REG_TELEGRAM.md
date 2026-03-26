# Guía oficial — Comando `/reg` por Telegram (factoría JISLAB)

Documento de referencia para **redactar requerimientos** que se registran con `/reg` en el bot de Telegram. El mismo criterio aplica si usás la UI **`jis-reg-ui`** o el script `factory_reg_post.py`: lo importante es el **texto del requerimiento** (lo que va **después** de `/reg`).

---

## 1. Qué es `/reg` y qué no es

| Es | No es |
|----|--------|
| Alta de un trabajo para la **factoría** (DTR + issue GitHub + cola Dev_JIS). | Un chat con el modelo para “idear” sin criterio de cierre. |
| Un **contrato técnico mínimo** para generar código y tests en sandbox. | Un reemplazo del diseño de producto completo ni del despliegue a producción. |
| Entrada idónea para tareas **acotadas** (módulo, funciones, tests verificables). | Pedidos vagos del estilo “mejorar el sistema” o “arreglar bugs” sin alcance. |

Tras el registro, el **factory-runner** (Aider + pytest) intenta implementar lo descrito. Si el texto es ambiguo o enorme, el resultado será peor o quedará **Blocked**.

---

## 2. Formato en Telegram

1. Un solo mensaje (o el primero de una serie coherente si el bot concatena).
2. Primera línea o inicio: **`/reg`** (con espacio después).
3. **Todo lo que sigue** a `/reg` es el cuerpo del requerimiento: será el `raw_text` del intake y base del DTR.

**Correcto**

```text
/reg Implementar en src/jis_foo.py una función bar(x: int) -> int que devuelva x*2. Tests en tests/test_jis_foo.py con pytest para x=0 y x=3.
```

**Incorrecto**

- Incluir otro comando antes: `hola /reg ...` (según bot, solo se procesa si el mensaje **empieza** con `/reg`).
- Repetir `/reg` dentro del texto del requerimiento.
- Mandar **solo** `/reg` sin descripción.

---

## 3. Estructura recomendada del texto (plantilla mental)

Convén ordenar el mensaje con secciones claras (podés usar títulos en español o inglés):

1. **Objetivo**  
   Una frase: qué problema resolvés o qué módulo agregás.

2. **Archivos / ubicación**  
   Rutas explícitas bajo el sandbox de factoría:
   - Código: `src/nombre_modulo.py` (o varios archivos si hace falta).
   - Tests: `tests/test_nombre_modulo.py`.

   > La factoría **detecta** rutas que coincidan con el patrón `src/...` y `tests/...` en el texto para pasarlas a Aider. **Nombralas siempre** así en el cuerpo del `/reg`.

3. **Comportamiento / API**  
   - Firmas de funciones o clases.  
   - Reglas de negocio y validaciones (qué valores son válidos, qué error esperado: `ValueError`, etc.).  
   - Fórmulas o algoritmos puntuales (ej. conversión °C→°F, redondeo a N decimales).

4. **Criterios de aceptación / tests**  
   Lista de casos que deben pasar con **pytest** (entradas → salidas o excepciones).  
   Cuanto más **testables** sea el texto, mejor cerrará el runner.

5. **Restricciones**  
   Ejemplos: “sin dependencias externas”, “usar Pydantic”, “persistencia en memoria con lista”, “no conectar a MySQL”, “código y nombres en inglés”, “PEP8”.

6. **Fuera de alcance (opcional)**  
   Una línea de lo que **no** debe hacer el cambio (evita que el modelo invente alcance).

---

## 4. Qué sí incluir

- Rutas **`src/...`** y **`tests/...`** con nombres de archivo realistas.
- **Tipos** (`str`, `int`, `float`, clases) cuando importe.
- **Casos límite** que quieras cubrir en tests.
- **Idioma del código**: si pedís inglés, decilo explícitamente.
- **Criterio de cierre**: “`pytest -q` debe pasar al 100% en el sandbox” (es el estándar del runner).

---

## 5. Qué no incluir

| Evitar | Por qué |
|--------|---------|
| Contraseñas, tokens, API keys, connection strings reales | Riesgo de seguridad y filtrado en GitHub/logs. |
| Datos personales reales (DNI, mails de clientes) | Privacidad; usá datos ficticios. |
| “Refactorizar todo el ERP” / “migrar a microservicios” | Alcance inmanejable para un solo ciclo de factoría. |
| Instrucciones contradictorias | El modelo y pytest no pueden “adivinar” la verdad. |
| Depender de servicios externos no mockeados | El sandbox no garantiza red ni servicios de prod. |
| Pedir solo documentación sin código ejecutable | El pipeline está orientado a **código + tests**. |

---

## 6. Ejemplos

### 6.1 Ejemplo brece (adecuado)

```text
/reg Objetivo: utilidad matemática mínima.
Archivo: src/jis_math.py con add_numbers(a: int, b: int) -> int y get_factory_name() -> str devolviendo exactamente "JISLAB-FACTORY-v1".
Tests: tests/test_jis_math.py con pytest: (1) add_numbers(5,7)==12 (2) get_factory_name()=="JISLAB-FACTORY-v1".
Sin dependencias externas. Código en inglés.
```

### 6.2 Ejemplo con validaciones (adecuado)

```text
/reg Módulo src/jislab_assets.py: clase AssetManager con método add_asset(name: str, type: str, cores: int). Validar: name no vacío; type en Server|Workstation|Network; cores entero > 0. Devolver dict con id UUID y campos. Lista en memoria para persistencia temporal. Pydantic para esquemas si aplica.
Tests tests/test_jislab_assets.py: caso OK Server 16 cores; ValueError si type Laptop; ValueError si cores 0.
pytest debe pasar 100%.
```

### 6.3 Ejemplo mal redactado (evitar)

```text
/reg Que el sistema ande mejor y sea más rápido.
```

No hay archivos, ni comportamiento medible, ni tests.

---

## 7. Qué pasa después del `/reg` (expectativas)

1. Recibís **REQ-…** e **issue** en GitHub (el bot puede mostrar un estado inicial; el flujo real puede pasar a **In Progress** y **Done** automáticamente).
2. El **factory-runner** genera código bajo `/workspaces/dev-jis-work/<REQ>/`.
3. Si **pytest** falla, el estado puede ir a **Blocked** hasta corregir o reintentar.
4. Código listo para revisión humana y, si aplica, **export** a repo (p. ej. `jislab-runtime`) con el script de export y PR.

La **producción** (VPS) es un paso **manual** aparte: merge en Git, despliegue y verificación en tu entorno.

---

## 8. Coherencia con el intake (referencia técnica)

El bot de Telegram suele construir un payload de intake con valores por defecto (p. ej. prioridad **P2**, módulo **otro**). **No podés cambiar eso desde el texto del `/reg`** salvo que el integrador del bot mapee campos adicionales. Por eso **toda la especificación técnica debe vivir en el texto libre** después de `/reg`.

Esquema JSON de referencia del mensaje completo (no lo enviás vos en Telegram; lo usa el backend): [`.agents/Req_JIS/intake-message-schema.json`](../.agents/Req_JIS/intake-message-schema.json).

---

## 9. Resumen checklist (antes de enviar)

- [ ] Empieza con `/reg` y tiene **cuerpo** suficiente.
- [ ] Menciona **`src/...`** y **`tests/...`** explícitos.
- [ ] Lista comportamiento y **casos de prueba** o criterios medibles.
- [ ] Restricciones claras (deps, idioma, sin DB, etc.).
- [ ] Sin secretos ni PII real.
- [ ] Alcance acotado a **un** entregable lógico.

---

## 10. Documentos relacionados

- Flujo completo factoría (README raíz, GitHub): [README.md](../README.md)  
- Mapa OpenClaw / rutas de config: [openclaw-jislab-map.md](openclaw-jislab-map.md)  
- Estados y cola Dev_JIS: [GOVERNANCE_STATE_ACTORS.md](GOVERNANCE_STATE_ACTORS.md)  
- UI web alternativa (sin chat OpenClaw): [WEB_REG_Y_OPENCLAW.md](WEB_REG_Y_OPENCLAW.md)  
- Actualizar OpenClaw (quitar aviso de versión): [PASOS_ACTUALIZAR_OPENCLAW.md](PASOS_ACTUALIZAR_OPENCLAW.md)  

**Versión:** 1.0 · Uso interno JISLAB factoría.
