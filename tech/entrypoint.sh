#!/bin/bash

poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 8000 tech.core.app.app:app