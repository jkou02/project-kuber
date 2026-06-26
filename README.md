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

## Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.12+ (solo si prefieres correr fuera de Docker)

## Estado del proyecto

- **Modelos de base de datos:** implementados (MVP).
- **Servicios y repositorios:** implementados para usuarios y transacciones.
- **Bot de Telegram:** funcional. Comandos disponibles: `/start`, `/quick`, `/add`, `/summary`.
- **API web:** en desarrollo inicial. Endpoint `/health` disponible.

## Instalación y setup

1. Clonar el repositorio.
2. Copiar el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```
3. Editar `.env` y asignar al menos `TELEGRAM_BOT_TOKEN`.
4. Levantar los servicios:
   ```bash
   docker compose up --build
   ```
   Esto inicia PostgreSQL, la API (puerto `8001`) y el bot.

5. Ejecutar migraciones de base de datos:
   ```bash
   docker compose exec api alembic upgrade head
   ```

## Comandos del bot

| Comando | Descripción |
|---|---|
| `/start` | Registra al usuario y da la bienvenida. |
| `/quick <tipo> <monto> <moneda> <categoría> [descripción]` | Registro rápido en lenguaje natural. Ejemplo: `/quick gasto 5 USD comida almuerzo` |
| `/add` | Registro paso a paso (conversación guiada). |
| `/summary` | Resumen del mes actual. |

## Desarrollo local

- **Levantar todo:** `docker compose up --build`
- **Ver logs:** `docker compose logs -f api bot`
- **Migrar DB:** `docker compose exec api alembic upgrade head`
- **Crear migración:** `docker compose exec api alembic revision --autogenerate -m "descripcion"`
- **Linter:** `docker compose exec api ruff check .`
- **Type checker:** `docker compose exec api mypy .`

### Sin Docker

Requiere Python 3.12+ y PostgreSQL 15+ corriendo localmente.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Configurar PostgreSQL local y ajustar DATABASE_URL
alembic upgrade head
```

Para ejecutar componentes individualmente:
```bash
# API
uvicorn api.main:app --reload

# Bot
python -m bot.main
```

## Arquitectura

El proyecto está organizado por dominio:

```
├── api/          # Routers y schemas FastAPI (en desarrollo inicial)
├── bot/          # Handlers y flujos conversacionales de Telegram (funcionales)
├── services/     # Reglas de negocio (usuarios y transacciones implementados)
├── repositories/ # Acceso a datos
├── models/       # Entidades SQLAlchemy (implementadas)
├── core/         # Configuración, base de datos y utilidades compartidas
├── migrations/   # Migraciones Alembic
└── tests/        # Pruebas con pytest (pendientes)
```

## Variables de entorno

Copia `.env.example` a `.env` y configura al menos:

| Variable            | Descripción                                      |
|---------------------|--------------------------------------------------|
| `DATABASE_URL`      | URL de conexión a PostgreSQL                     |
| `TELEGRAM_BOT_TOKEN`| Token del bot de Telegram (de @BotFather)        |
| `SECRET_KEY`        | Clave secreta para futura autenticación / JWT    |
| `ENVIRONMENT`       | `development`, `staging` o `production`          |

## Testing

El proyecto usa `pytest` con soporte async. Configurado en `pyproject.toml`:

```bash
pytest
```

> Actualmente no hay tests escritos. Esta sección se actualizará conforme se agreguen.

## Licencia

[GPL-3.0](LICENSE)
