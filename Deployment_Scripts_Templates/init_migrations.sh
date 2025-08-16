#!/bin/bash
echo "🧱 Running DB migrations..."
alembic upgrade head
