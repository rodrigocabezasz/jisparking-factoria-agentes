# GitHub Project v2 - Configuracion para Factoria OpenClaw

## 1. Objetivo

Establecer GitHub Project v2 como fuente de verdad de estado para la factoría de desarrollo.

## 2. Vistas recomendadas

- Vista Kanban por Estado
- Vista Tabla por Prioridad y SLA
- Vista Riesgo/Security
- Vista Aging (items no movidos por N dias)

## 3. Columnas de Kanban

- Backlog
- Ready
- In Progress
- In Review
- QA
- Blocked
- Done

## 4. Campos personalizados

1. RequestID (text)
2. Priority (single select: P0, P1, P2, P3)
3. Site (single select: IntraJIS, JISReportes, Integracion, Infra)
4. Module (single select: auth, ventas, facturacion, contabilidad, pagos, dashboard, api, infra, db, otro)
5. Risk (single select: alto, medio, bajo)
6. SLA Response Hours (number)
7. SLA Resolution Hours (number)
8. Owner Team (single select: Req, Dev, QA_Doc, Security)
9. State (single select: Backlog, Ready, In Progress, In Review, QA, Blocked, Done)

## 5. Reglas de automatizacion recomendadas

1. Al crear issue con label status:backlog -> State=Backlog
2. Al agregar label status:ready -> State=Ready
3. Al abrir PR vinculada -> State=In Review
4. Al mergear PR -> State=QA
5. Al agregar label qa:passed -> State=Done
6. Al agregar label status:blocked -> State=Blocked

## 6. Convencion de etiquetas

- type:feature
- type:bug
- type:chore
- status:backlog
- status:ready
- status:in-progress
- status:review
- status:qa
- status:blocked
- status:done
- priority:P0
- priority:P1
- priority:P2
- priority:P3
- risk:high
- risk:medium
- risk:low
- security:pii
- security:finanzas
- security:credenciales
- security:acceso
- security:fraude

## 7. SLA sugerido

- P0: respuesta 1h, resolucion 24h
- P1: respuesta 4h, resolucion 72h
- P2: respuesta 8h, resolucion 120h
- P3: respuesta 24h, resolucion 240h

## 8. KPIs minimos

- Lead Time promedio
- Cycle Time por estado
- Throughput semanal
- Tasa de bloqueos
- Aging promedio por estado
- Reaperturas

## 9. Regla de oro operacional

El estado en Project debe coincidir con evidencia real:

- si hay PR abierta, no puede quedar en Backlog
- si QA no ha validado, no puede pasar a Done
