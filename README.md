# KuberCalc

Sistema personal de finanzas con enfoque **Telegram-first** para el registro rápido de ingresos y gastos.

## ¿Qué es KuberCalc?

KuberCalc es una aplicación backend pensada para reemplazar hojas de cálculo manuales por un sistema real de base de datos, accesible principalmente a través de un bot de Telegram. Prioriza la **rapidez de captura** y la **constancia** sobre la completitud de campos.

## Características principales (MVP)

- Registro de ingresos y gastos en bolívares (Bs) y dólares (USD).
- Categorías, métodos de pago y fuentes de ingreso configurables.
- Presupuestos mensuales por categoría con comparación contra gasto real.
- Resumen automático del mes: ingresos, gastos, flujo neto.
- Movimientos recientes, edición y eliminación fácil.
- Registro rápido en lenguaje natural desde Telegram.

## Stack tecnológico

- **Python 3.12+**
- **FastAPI** — API/backend principal.
- **PostgreSQL 15+** — base de datos persistente.
- **SQLAlchemy 2.0 / SQLModel** — ORM y modelado.
- **Pydantic v2** — validación de datos.
- **Alembic** — migraciones de base de datos.
- **python-telegram-bot (v20+)** — bot async de Telegram.
- **Docker Compose** — desarrollo local.

## Arquitectura

El proyecto está organizado por dominio:

```
├── api/          # Routers y schemas FastAPI
├── bot/          # Handlers y flujos conversacionales de Telegram
├── services/     # Reglas de negocio
├── repositories/ # Acceso a datos
├── models/       # Entidades SQLAlchemy
├── core/         # Configuración y utilidades compartidas
└── tests/        # Pruebas con pytest
```

## Variables de entorno

Copia `.env.example` a `.env` y configura al menos:

- `DATABASE_URL`
- `TELEGRAM_BOT_TOKEN`
- `SECRET_KEY`
- `ENVIRONMENT`

## Licencia

[GPL-3.0](LICENSE)
