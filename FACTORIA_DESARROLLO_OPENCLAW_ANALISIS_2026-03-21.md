# Factoria de Desarrollo OpenClaw - Analisis Real y Diseno Objetivo

Fecha: 2026-03-21
Alcance: Revision de lo ya implementado en servidor jislab y propuesta de optimizacion de la factoria de agentes para desarrollo.

## 1. Respuesta Directa a tu Duda

Si, tu planteamiento es correcto.

La forma mas robusta de operar esta factoria es:

- Tener OpenClaw + Intake como capa de orquestacion.
- Tener un entorno de desarrollo unificado en Docker para que los agentes ejecuten trabajo tecnico de forma consistente.
- Mantener todo trazado en GitHub Issues + GitHub Projects (Kanban) con estados y evidencia automatizada.

Conclusion practica:

- No conviene dejar cada tecnologia dispersa en el host.
- Conviene una plataforma contenida y repetible (contenedores de trabajo por solicitud, usando imagen base estandar).

## 2. Evidencia Revisada (Servidor OpenClaw real)

Esta evaluacion se hizo sobre artefactos reales en OpenClaw por SSH, no solo con notas locales.

Componentes confirmados:

- OpenClaw corriendo en docker-compose con volumen persistente data.
- Servicio jis-intake (FastAPI) activo.
- Definicion de agentes JIS existente en .agents:
  - Req_JIS
  - Ingeniero_Principal_JIS
  - Dev_JIS
  - QA_Doc_JIS
  - Security_JIS
- Contrato formal de intake en JSON Schema:
  - .agents/Req_JIS/intake-message-schema.json
- Generacion de DTR automatica confirmada:
  - apps/jis-agent-sandbox/runs/dtr/REQ-\*.md
- Integracion GitHub activa en intake:
  - creacion de issue via API de GitHub en app/main.py
- Pipeline basico de estado y metricas:
  - endpoint /events/state-change
  - endpoint /metrics/summary

## 3. Como Funciona Hoy (AS-IS)

Flujo actual observado:

1. Llega mensaje por API /intake o /telegram/webhook.
2. Se valida payload con JSON Schema.
3. Se genera archivo DTR markdown en runs/dtr.
4. Se crea issue en GitHub (si token/repo configurados).
5. Se guarda estado en SQLite (requests/events).
6. Se puede actualizar estado por API y consultar metricas resumen.

Fortalezas actuales:

- Ya existe una base funcional de factoria.
- Existe tipificacion de entrada (schema), esto es clave.
- Existe trazabilidad minima request -> DTR -> issue.
- Ya hay perfiles de agentes bien definidos por rol.

## 4. Brechas Reales (lo que falta para ser factoría madura)

### 4.1 Brecha de calidad de especificacion

Problema:

- El webhook de Telegram actualmente asigna valores por defecto muy genericos (site, impact, priority, module), lo que puede degradar la calidad del issue.

Impacto:

- Mucho trabajo posterior de aclaracion.
- Riesgo de backlog ruidoso.

Mejora:

- Clasificador de requerimiento con reglas + LLM de normalizacion.
- Gating: si faltan campos criticos, pedir aclaracion controlada antes de emitir issue.

### 4.2 Brecha de DTR insuficiente

Problema:

- El DTR actual es util pero corto; deja pasos manuales para completar plantilla oficial.

Impacto:

- Requiere edicion humana frecuente.
- Inconsistencia entre tickets.

Mejora:

- DTR completo auto-generado con secciones obligatorias:
  - contexto de negocio
  - alcance/no alcance
  - RF/RNF
  - criterios de aceptacion en Given/When/Then
  - riesgos
  - plan de pruebas
  - impacto en arquitectura y datos

### 4.3 Brecha de Kanban automatizado

Problema:

- Existe seguimiento de estado, pero no se observa integracion completa de GitHub Project como fuente de verdad operacional.

Impacto:

- Estado duplicado o desalineado entre sistema interno y tablero.

Mejora:

- GitHub Project v2 como control central.
- Automatizaciones por evento issue/PR/merge.

### 4.4 Brecha de entorno de ejecucion para agentes Dev

Problema:

- Aun no esta consolidado un contenedor de trabajo estandar para ejecutar desarrollos por requerimiento.

Impacto:

- Entornos heterogeneos y resultados menos reproducibles.

Mejora:

- Crear image factory-runner con stack completo (python/node/tools devops/tests).
- Ejecutar trabajos de agentes en workspaces aislados por solicitud.

### 4.5 Brecha de seguridad operativa

Problema:

- Ya hubo exposicion de secretos en texto plano en artefactos de trabajo.

Impacto:

- Riesgo de compromiso de cuentas/repositorios.

Mejora:

- Secret manager por entorno.
- Politica de rotacion.
- Escaneo de secretos en CI.

## 5. Diseno Objetivo (TO-BE)

## 5.1 Arquitectura de la factoria

Capas:

1. Capa de Entrada

- OpenClaw chat
- Telegram webhook

2. Capa de Orquestacion

- Req_JIS clasifica y normaliza
- Genera DTR completo
- Crea issue + item en GitHub Project

3. Capa de Ejecucion Tecnica

- Contenedor factory-runner por solicitud (workspace aislado)
- Agentes Dev/QA/Security/Docs trabajan sobre repos Git

4. Capa de Gobierno

- GitHub Issues + PR + Projects (Kanban)
- Reglas de estado, SLA y trazabilidad

5. Capa de Evidencia

- Artefactos: DTR, plan de pruebas, resultados, ADR, changelog
- Metricas de flujo y calidad

## 5.2 Flujo operativo recomendado

1. Mensaje entra por OpenClaw o Telegram.
2. Gate de clasificacion determina si es requerimiento formal o consulta.
3. Si es requerimiento:

- generar RequestID
- normalizar campos criticos
- completar DTR tecnico
- validar DoR (Definition of Ready)

4. Crear Issue y asignar al Kanban (Backlog/Ready).
5. Ingeniero_Principal_JIS descompone en subtareas (Dev/QA/Sec/Doc).
6. Agente Dev ejecuta cambios en rama dedicada.
7. Agente QA genera/ejecuta pruebas y evidencia.
8. Agente Security valida controles y riesgos.
9. Agente Docs actualiza documentacion tecnica/operativa.
10. PR merge -> actualizacion automatica de estado a QA/Done.
11. Cierre con evidencia completa y metricas.

## 6. Docker Unificado para Desarrollo (propuesta concreta)

Tu idea es correcta: usar un entorno unico, consistente y versionado.

## 6.1 Servicios recomendados

- openclaw-gateway
- jis-intake
- factory-runner (nuevo)
- redis (cola de trabajos)
- postgres o sqlite robustecido (estado de orquestacion)

## 6.2 Rol de factory-runner

El factory-runner debe traer:

- Python 3.11+
- Node 22+
- git, gh CLI
- herramientas de test/lint
- utilidades de build para stacks JIS

Modo de ejecucion:

- Un workspace por request_id.
- Clonado repo destino.
- Ejecucion de tareas de agente (dev/test/doc/security).
- Publicacion de evidencia a GitHub (comentarios, checklists, archivos).

## 6.3 Aislamiento recomendado

- Evitar network_mode host para todo (solo cuando sea realmente necesario).
- Redes docker dedicadas por servicio.
- Volumenes controlados:
  - /workspaces/<request_id>
  - /artifacts/<request_id>

## 7. Gobierno en GitHub Projects (modelo Kanban)

Columnas recomendadas:

- Backlog
- Ready
- In Progress
- In Review
- QA
- Done
- Blocked

Campos recomendados:

- Priority (P0-P3)
- Site (IntraJIS/JISReportes/Integracion/Infra)
- Module
- Risk
- SLA target
- Owner
- RequestID

Automatizaciones minimas:

- Issue creada -> Backlog
- Label ready -> Ready
- PR abierta -> In Review
- PR mergeada -> QA
- Checklist QA ok -> Done
- Label blocked -> Blocked

## 8. Definition of Ready y Definition of Done

## 8.1 DoR (para iniciar desarrollo)

Debe existir:

- DTR completo
- criterios de aceptacion verificables
- alcance y no-alcance
- riesgo de seguridad clasificado
- repositorio/modulo objetivo definido

## 8.2 DoD (para cerrar)

Debe existir:

- codigo mergeado
- pruebas ejecutadas con evidencia
- documentacion actualizada
- riesgo residual declarado
- issue y project en estado final consistente

## 9. Roadmap de Mejora (sin romper lo que ya funciona)

Fase 1 - Estabilizacion (rapida)

- Fortalecer webhook Telegram: mejor normalizacion y validaciones.
- Ampliar DTR automatico a plantilla completa.
- Definir y aplicar DoR/DoD en issue template.

Fase 2 - Gobierno Kanban

- Configurar GitHub Project v2 con campos y automatizaciones.
- Sincronizar estado de API interna con estados del Project.

Fase 3 - Runner unificado Docker

- Crear imagen factory-runner versionada.
- Ejecutar trabajos por request en workspaces aislados.
- Publicar evidencia automatica a PR/Issue.

Fase 4 - Calidad y seguridad avanzada

- CI obligatoria por repo (lint/test/security scan/secret scan).
- Politicas de branch protection.
- Metricas de rendimiento de factoría (lead time, throughput, aging, blocked rate).

## 10. Veredicto Tecnico

Estas bien orientado.

Hoy ya tienen una base funcional real de factoría en OpenClaw.
Para convertirla en el alma de desarrollo que buscas, faltan 4 saltos:

1. Mejor normalizacion de requerimientos.
2. DTR realmente completo y accionable.
3. Kanban automatizado como control central.
4. Runner Docker unificado por solicitud para ejecucion tecnica reproducible.

Con esos pasos, el sistema pasa de piloto funcional a plataforma de desarrollo gobernada.

## 11. Siguiente paso recomendado inmediato

Implementar primero la Fase 1 + Fase 2 (menos riesgo, alto impacto):

- Subir calidad de intake/DTR.
- Cerrar el circuito de estados en GitHub Project.

Luego desplegar Fase 3 (factory-runner), que es donde se consolida el entorno unificado de desarrollo para agentes.
