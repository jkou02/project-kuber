# AGENTS.md

## Propósito
Actúa como un agente de desarrollo para un entorno de trabajo compartido.
Prioriza exactitud, seguridad, cambios fáciles de revisar y comunicación de bajo ruido.
Optimiza tus respuestas para ahorrar tokens sin perder claridad.

## Estilo de respuesta
- Responde de forma breve, directa y útil por defecto.
- Evita explicaciones largas si no fueron solicitadas.
- Cuando existan varias opciones válidas, recomienda una por defecto y justifícala brevemente.
- No repitas información ya presente en el repositorio o en la conversación.
- Si una respuesta puede resolverse en pocos pasos, prioriza el formato corto.

## Seguridad y aprobaciones
- Leer archivos e inspeccionar el repositorio está permitido por defecto.
- Antes de crear, editar, eliminar, mover o renombrar archivos, solicita aprobación, salvo que la configuración activa permita hacerlo sin confirmación.
- Antes de ejecutar comandos que modifiquen archivos, instalen dependencias, alteren Git o cambien el entorno, solicita aprobación, salvo que la configuración activa permita hacerlo.
- Nunca expongas, registres, pegues ni confirmes secretos, credenciales, tokens, llaves privadas o valores sensibles.
- Trata como sensibles los archivos `.env`, secretos de despliegue, credenciales, claves API y configuraciones de infraestructura.
- Prefiere acciones reversibles y cambios pequeños.

## Flujo de trabajo con Git
- Trabaja siempre con conciencia del estado actual del repositorio.
- Antes de proponer commits o cambios grandes, revisa el estado y el diff cuando sea relevante.
- Agrupa cambios relacionados y evita mezclar tareas no conectadas.
- Usa Conventional Commits para sugerir mensajes de commit.
- Formato preferido: `tipo(alcance): descripción corta`.
- Tipos comunes: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`.
- Usa `!` o un footer `BREAKING CHANGE:` cuando el cambio rompa compatibilidad.
- No hagas commits, merges, rebases, force-push ni cambios de rama a menos que el usuario lo solicite de forma explícita.
- Cuando resumas cambios, basa el resumen en el diff real.

## Higiene del código y del repositorio
- Prefiere nombres claros para variables, funciones, clases, archivos y módulos.
- Evita complejidad innecesaria, abstracciones prematuras y dependencias injustificadas.
- Respeta el estilo ya existente del repositorio cuando esté claro.
- Si el proyecto no tiene una convención evidente, prioriza legibilidad y simplicidad.
- Evita dejar archivos temporales, artefactos locales o resultados intermedios dentro del repositorio si no forman parte real del proyecto.
- Si detectas ausencia de `.gitignore` en un proyecto nuevo, sugiere crearlo.

## Variables de entorno y secretos
- Nunca hardcodees secretos o credenciales en el código fuente.
- Si el proyecto requiere variables de entorno, documenta las necesarias en `.env.example`.
- Mantén fuera del control de versiones los archivos locales con secretos o configuración sensible.
- Si agregas una nueva variable de entorno, explica brevemente su propósito.

## Validación antes de cerrar una tarea
- Antes de dar una tarea por terminada, identifica si existen pruebas, validaciones, linters o chequeos relevantes.
- Si puedes validarlos de forma segura y está permitido, ejecútalos.
- Si no puedes ejecutarlos, indícalo de forma explícita.
- Reporta de forma breve los supuestos, riesgos o partes pendientes.
- Prioriza cambios fáciles de revisar y revertir.

## Reglas de comunicación
- Si los requisitos no están claros, haz preguntas concretas antes de asumir.
- Si una tarea implica riesgo, dilo antes de ejecutar acciones sensibles.
- Si existe una alternativa mejor, menciónala brevemente en lugar de seguir una solución débil sin avisar.
- No inventes archivos, dependencias, APIs, rutas o comportamientos que no estén respaldados por el repositorio o por instrucciones del usuario.
- Si falta contexto crítico, dilo de forma directa.

## Extensión por stack o proyecto
- Las reglas específicas del stack, arquitectura, comandos de desarrollo, pruebas y despliegue deben definirse en archivos del proyecto o módulos adicionales.
- Este archivo establece reglas universales; las instrucciones específicas deben extenderlo, no reemplazarlo.

---

# Contexto del proyecto: KuberCalc

## Stack y herramientas
- **Lenguaje:** Python 3.12+
- **Framework web:** FastAPI
- **ORM / modelado:** SQLAlchemy 2.0 + SQLModel donde aplique
- **Validación:** Pydantic v2
- **Base de datos:** PostgreSQL 15+
- **Migraciones:** Alembic
- **Bot de Telegram:** python-telegram-bot (v20+, async)
- **Contenedores:** Docker Compose para desarrollo local
- **Testing:** pytest (a definir estructura de tests)
- **Configuración:** python-dotenv, archivo `.env.example` obligatorio

## Arquitectura esperada
- Backend modular organizado por dominio (no por capa técnica pura).
- Separar claramente:
  - `api/` — routers y schemas FastAPI.
  - `bot/` — handlers, comandos y flujos conversacionales de Telegram.
  - `services/` — reglas de negocio, orquestación entre repositorios.
  - `repositories/` — acceso a datos vía ORM.
  - `models/` — entidades de base de datos (SQLAlchemy).
  - `core/` — configuración, utilidades y excepciones compartidas.
- El bot y la API pueden convivir en el mismo proceso o en servicios separados, pero comparten `services`, `repositories` y `models`.
- Preparar la estructura para que un panel web futuro reutilice la misma API.

## Entidades principales del dominio
La fuente de verdad es `transactions`. Las entidades esperadas son:
- `users`
- `transactions` (ingresos y gastos, multimoneda, con tasa de cambio)
- `categories`
- `payment_methods`
- `income_sources`
- `monthly_budgets`
- `savings_goals` (fase 2)
- `debts` y `debt_payments` (fase 2)
- `exchange_rates`
- `tags` o `labels` (opcional)
- `recurring_templates` (opcional, fase 2)

## Principios de diseño prioritarios
1. **Rapidez de captura por encima de completitud:** el registro mínimo debe ser mínimo; enriquecimiento posterior permitido.
2. **Multimoneda desde el inicio:** Bs y USD con tasa de cambio por movimiento; no como parche posterior.
3. **Una sola fuente de verdad:** los reportes y dashboards se calculan a partir de `transactions`, no se duplican.
4. **Telegram-first:** comandos claros, respuestas breves, flujos simples, usable desde teléfono.

## Flujos de Telegram clave a respetar
- `/start` — bienvenida y configuración inicial.
- `/add` — registro paso a paso.
- `/quick` — registro en lenguaje natural (ej. `gasto 5 USD comida almuerzo`).
- `/summary` — resumen del mes (ingresos, gastos, flujo neto).
- `/budget` — presupuesto vs realidad por categoría.
- `/recent` — movimientos recientes.
- `/edit` y `/delete` — corrección fácil del último o movimientos recientes.
- `/categories`, `/methods` — administración básica.
- `/goals`, `/debts` — fase 2.

## Variables de entorno sensibles típicas
- `DATABASE_URL`
- `TELEGRAM_BOT_TOKEN`
- `SECRET_KEY` (para futura autenticación / JWT)
- `ENVIRONMENT` (dev / staging / prod)

## Convenciones de commit para este proyecto
Usar Conventional Commits con alcances representativos del dominio, por ejemplo:
- `feat(transactions): agrega registro rápido en lenguaje natural`
- `fix(budget): corrige cálculo de presupuesto vs gasto real`
- `refactor(bot): extrae handlers a módulo separado`
- `chore(db): agrega migración inicial de tablas core`

## MVP y fases
- **MVP:** transacciones, categorías, métodos de pago, presupuestos mensuales, resúmenes por Telegram.
- **Fase 2:** metas de ahorro, deudas, abonos, recordatorios, sugerencias de categorización, panel web.
- No implementar fase 2 antes de que el MVP esté funcional y probado.