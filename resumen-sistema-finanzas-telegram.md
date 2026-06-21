# Resumen para OpenCode: sistema personal de finanzas

Quiero construir un sistema personal de finanzas inspirado en mi hoja de cálculo actual llamada `Manejo-de-presupuesto-2025.xlsx`, que uso para llevar mi presupuesto personal. [file:1] La lógica actual de esa hoja incluye registro de ingresos y gastos, categorías, métodos de pago, montos en bolívares y dólares, tasa de cambio por movimiento, presupuesto mensual por categoría, metas de ahorro, deudas y un dashboard con métricas como ingresos del mes, gastos del mes, flujo neto, tasa de ahorro, deuda total y comparación entre presupuesto y gasto real. [file:1]

El problema principal que quiero resolver no es solo el análisis financiero, sino la fricción al registrar los movimientos. Mi sistema en Excel/Google Sheets es bastante completo, pero dejó de ser práctico porque registrar manualmente cada gasto tomaba demasiado esfuerzo, y eso hacía que se me olvidara anotar movimientos durante días o incluso durante todo el mes. Por eso, el nuevo sistema debe estar diseñado con enfoque “Telegram-first”: registrar gastos e ingresos debe ser extremadamente rápido, simple y posible desde cualquier lugar mediante un bot de Telegram.

## Objetivo del sistema

El sistema debe reemplazar la lógica principal de `Manejo-de-presupuesto-2025.xlsx` sin copiar literalmente la hoja de cálculo. [file:1] Debe conservar la esencia funcional: transacciones, categorías, presupuestos mensuales, metas, deudas y resúmenes automáticos; pero rediseñado como una aplicación real, con base de datos y flujos rápidos desde Telegram. [file:1]

El sistema debe considerar que la hoja actual maneja:

- Movimientos con fecha, descripción, tipo, método de pago o fuente, categoría, monto en Bs, monto en USD y referencia del dólar. [file:1]
- Categorías como Alimentación, Transporte, Vivienda, Gastos Personales, Mascota - Light, Novia, Prestamos, Comisión, Viaje, Deudas, Gimnasio y otras. [file:1]
- Fuentes de ingreso o clasificación de ingresos como Salario, Mamá, Otros y Devolución de Prestamo. [file:1]
- Presupuesto mensual por categoría con comparación entre “presupuestado” y “gastado”. [file:1]
- Métricas de dashboard como ingresos mensuales, gastos mensuales, flujo neto, tasa de ahorro, deuda total y total ahorrado para metas. [file:1]
- Seguimiento de metas de ahorro y una sección para deudas. [file:1]

## Stack tecnológico

Quiero usar:

- Python para el backend.
- PostgreSQL para la base de datos.
- Un bot de Telegram como interfaz principal de uso remoto.
- Una arquitectura modular y mantenible, preparada para crecer más adelante.
- Posibilidad futura de agregar un panel web, pero eso no debe ser prioridad en la primera versión.

## Recomendaciones de diseño

No quiero que el sistema replique todas las complejidades del Excel desde el día uno. La nueva aplicación debe estar diseñada alrededor de una sola fuente de verdad: una tabla principal de transacciones. [file:1] Casi todos los análisis de la hoja actual salen de los movimientos registrados y luego se resumen por mes, categoría o dashboard, por lo que el sistema debe calcular los reportes a partir de esos datos en lugar de guardar resultados duplicados. [file:1]

También quiero que el diseño priorice rapidez de captura por encima de cantidad de campos obligatorios. En la hoja actual cada movimiento puede tener bastante detalle, pero en la práctica eso hace más lenta la carga manual; por eso, el sistema debería permitir registrar primero lo mínimo y luego editar o enriquecer el movimiento después. [file:1]

Se recomienda que el sistema nazca con estas decisiones de producto:

- El registro mínimo debe pedir solo: tipo, monto, moneda, categoría, método de pago, descripción corta y fecha.
- La tasa de cambio debe poder ser opcional o autocompletarse si el movimiento es en Bs y se quiere convertir a USD.
- Debe existir un modo de registro rápido en lenguaje natural.
- Debe permitirse editar o corregir movimientos recientes fácilmente.
- Debe haber recordatorios opcionales por Telegram para no abandonar el hábito.
- El dashboard debe ser automático; la idea es registrar movimientos y que el sistema produzca los resúmenes.

## Funcionalidades MVP

Primera versión:

- Registrar ingresos y gastos desde Telegram.
- Consultar resumen del mes actual.
- Consultar gastos por categoría.
- Comparar presupuesto mensual vs gasto real por categoría.
- Ver movimientos recientes.
- Editar o eliminar movimientos recientes.
- Administrar categorías, métodos de pago y fuentes de ingreso.
- Registrar presupuestos mensuales por categoría.

Segunda fase:

- Metas de ahorro.
- Gestión de deudas.
- Abonos a deudas.
- Recordatorios automáticos.
- Reglas o sugerencias automáticas de categorización.
- Panel web administrativo.

## Arquitectura sugerida

Quiero que se proponga una arquitectura backend clara, usando Python, idealmente con FastAPI, organizada por módulos de dominio. La aplicación debería incluir:

- API/backend principal.
- Servicio del bot de Telegram.
- Capa de servicios para reglas de negocio.
- Capa de acceso a datos con ORM.
- PostgreSQL como almacenamiento persistente.
- Migraciones con Alembic.
- Configuración con variables de entorno.
- Docker Compose para desarrollo local.

## Modelo de datos sugerido

Quiero que se proponga y luego se implemente un modelo de base de datos con entidades como:

- `users`
- `transactions`
- `categories`
- `payment_methods`
- `income_sources`
- `monthly_budgets`
- `savings_goals`
- `debts`
- `debt_payments`
- `exchange_rates`
- `tags` o labels opcionales
- `recurring_templates` opcional para movimientos repetitivos

La entidad más importante debe ser `transactions`, porque será la fuente principal de verdad del sistema. [file:1] Debe soportar ingresos y gastos, múltiples monedas, tasas de cambio por movimiento, categorías y método de pago o fuente. [file:1]

## Flujos de Telegram

Quiero que el bot de Telegram tenga comandos o flujos como estos:

- `/start` para bienvenida y configuración inicial.
- `/add` para registrar un nuevo movimiento paso a paso.
- `/quick` para registrar un movimiento en una sola línea, por ejemplo: `gasto 5 USD comida almuerzo`.
- `/summary` para mostrar ingresos, gastos y flujo neto del mes.
- `/budget` para ver presupuesto vs realidad por categoría.
- `/recent` para listar movimientos recientes.
- `/edit` para corregir un movimiento reciente.
- `/delete` para borrar un movimiento.
- `/categories` para administrar categorías.
- `/methods` para administrar métodos de pago.
- `/goals` para ver metas de ahorro.
- `/debts` para ver o registrar deudas.

El bot debe ser usable desde teléfono, con respuestas claras, breves y flujos simples. La prioridad es reducir al máximo la fricción de uso.

## Requisitos técnicos

Quiero que el proyecto cumpla con estas buenas prácticas:

- Código limpio, modular y mantenible.
- Uso de SQLAlchemy o SQLModel.
- Validación con Pydantic.
- Alembic para migraciones.
- Docker Compose para levantar backend y PostgreSQL.
- Estructura preparada para pruebas.
- Archivo `.env.example`.
- Separación clara entre configuración, modelos, repositorios, servicios y handlers del bot.
- Preparación para añadir autenticación, panel web y analítica más adelante.

## Lo que se espera de OpenCode

Quiero que OpenCode trabaje por etapas:

1. Analizar este requerimiento y proponer una arquitectura del proyecto.
2. Diseñar el esquema de base de datos.
3. Proponer los casos de uso del bot de Telegram.
4. Definir el MVP y lo que debe dejarse para fase 2.
5. Generar el scaffold inicial del proyecto.
6. Implementar primero el módulo de transacciones, categorías, métodos de pago y presupuestos mensuales.
7. Después agregar resúmenes mensuales y consultas por Telegram.
8. Finalmente dejar preparado el sistema para metas de ahorro y deudas.

## Observaciones importantes

No quiero una copia visual de Excel. Quiero un sistema mejor pensado para uso diario. [file:1] Mi hoja `Manejo-de-presupuesto-2025.xlsx` demuestra que necesito flexibilidad para registrar movimientos en Bs y USD, agrupar por categorías, llevar presupuestos mensuales y calcular métricas financieras, pero el nuevo sistema debe optimizarse para constancia, rapidez y facilidad de uso desde Telegram. [file:1]

También quiero que se tome en cuenta que hay movimientos repetitivos o parecidos en mi historial, por ejemplo gastos de alimentación, transporte, vivienda, comisiones, gastos personales y pagos frecuentes, así que sería ideal dejar abierta la posibilidad de crear plantillas, autocompletado o sugerencias inteligentes más adelante. [file:1]

## Recomendaciones finales

- La recomendación principal es que el MVP se enfoque en 4 piezas: transacciones, categorías, presupuestos mensuales y resúmenes. [file:1]
- Metas y deudas sí deben considerarse en el diseño, porque existen en la hoja actual, pero conviene dejarlas como segunda etapa para no frenar el arranque. [file:1]
- También se recomienda implementar desde el inicio un flujo de “registro rápido” y otro de “editar último movimiento”, porque ahí estará gran parte del valor real del sistema.
- Como el archivo ya maneja montos en bolívares, dólares y referencia del dólar por operación, conviene modelar bien la multimoneda desde el principio y no como parche posterior. [file:1]
