**Quick Start (Infrastructure + API)**

Make sure Docker Desktop is running and your Python virtual environment is activated.

Start infrastructure (MongoDB + Redis): docker compose up -d

Start the API (Flask): python -m api.app

Stop everything: docker compose down