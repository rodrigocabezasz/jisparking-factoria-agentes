# Plan de Ejecucion - Factoria OpenClaw (Fase 1 y 2)

Fecha: 2026-03-21
Objetivo: Pasar de piloto funcional a operacion gobernada para desarrollo.

## 1. Estado de Acceso (resuelto)

Se validó conexion SSH sin password con llave desde notebook a jislab.
Pruebas exitosas:

- Alias: ssh jislab
- IP: ssh jislab@192.168.0.5

Resultado: flujo operativo mas rapido para auditoria y cambios.

## 2. Fase 1 - Calidad de Intake y DTR

## 2.1 Meta

Subir calidad del requerimiento antes de crear issue, reduciendo ambiguedad y retrabajo.

## 2.2 Tareas

1. Definir contrato ampliado de DTR

- Secciones obligatorias:
  - contexto
  - alcance/no alcance
  - RF/RNF
  - criterios de aceptacion Given/When/Then
  - riesgos
  - plan de pruebas
  - impacto de datos y seguridad

2. Mejorar normalizacion Telegram/OpenClaw

- Clasificar automaticamente:
  - site
  - module
  - priority
  - impact
- Si faltan datos criticos: pedir aclaracion minima controlada.

3. Introducir gate DoR antes de issue

- Si no cumple DoR, no crear issue y dejar estado Analisis.

4. Generar issue con plantilla robusta

- Incluir checklist de DEV/QA/SEC/DOC.
- Incluir referencia al DTR.

## 2.3 Criterios de exito

- Menos issues con descripcion incompleta.
- Disminucion de tickets reabiertos por ambiguedad.
- DTR completos en al menos 90 por ciento de ingresos.

## 3. Fase 2 - Gobierno Kanban en GitHub Projects

## 3.1 Meta

Usar GitHub Project como fuente de verdad del estado de ejecucion.

## 3.2 Estructura recomendada

Columnas:

- Backlog
- Ready
- In Progress
- In Review
- QA
- Blocked
- Done

Campos:

- RequestID
- Priority
- Site
- Module
- Risk
- SLA
- Owner

## 3.3 Automatizaciones minimas

1. Issue creada -> Backlog
2. Label ready -> Ready
3. PR abierta -> In Review
4. Label qa-passed o checklist QA completa -> Done
5. Label blocked -> Blocked

## 3.4 Integracion con estado interno

- Sincronizar endpoint de estado con Project:
  - /events/state-change debe reflejar transicion equivalente en tablero.
- Evitar doble fuente de estado no sincronizada.

## 3.5 Criterios de exito

- Estado consistente entre issue, PR y project.
- Tiempo de ciclo visible por etapa.
- Aging de tarjetas detectable.

## 4. Roles en la Factoria (operacion)

- Req_JIS: intake, clarificacion, DTR y DoR.
- Ingeniero_Principal_JIS: priorizacion, handoff y bloqueos.
- Dev_JIS: implementacion y evidencia tecnica.
- QA_Doc_JIS: pruebas, regresion, runbook y docs.
- Security_JIS: controles y riesgos de seguridad.

## 5. Entregables de cierre de Fase 1 y 2

1. Plantilla DTR v2 activa.
2. Plantilla issue y PR con checklists.
3. Project Kanban configurado con campos y reglas.
4. Matriz de transiciones de estado documentada.
5. Reporte base semanal de metricas de flujo.

## 6. Riesgos y mitigaciones

Riesgo 1: intake sobrecargado de defaults.

- Mitigacion: reglas de clasificacion + gate DoR.

Riesgo 2: estado desalineado entre sistemas.

- Mitigacion: sincronizacion automatica contra GitHub Project.

Riesgo 3: secretos expuestos en operacion.

- Mitigacion: secret manager + rotacion + secret scanning en CI.

## 7. Siguiente paso inmediato

Semana 1:

- activar DTR v2
- aplicar DoR
- crear templates issue/PR

Semana 2:

- configurar Project v2 y automatizaciones
- habilitar reporte de metricas de flujo

Con esto quedara lista la base gobernada para pasar a Fase 3 (factory-runner Docker por solicitud).

## 8. Artefactos creados en este workspace

- .github/ISSUE_TEMPLATE/requerimiento-factoria.yml
- .github/pull_request_template.md
- plantillas/dtr-template-v2.md
- factoria/github-project-v2-setup.md
- factoria/project-automation-matrix.csv

Uso recomendado:

1. Copiar templates de .github al repositorio que usara la factoria.
2. Activar dtr-template-v2 como plantilla base del intake.
3. Configurar GitHub Project v2 siguiendo github-project-v2-setup.md.
4. Cargar project-automation-matrix.csv como guia de reglas/automatizaciones.
