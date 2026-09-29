## STEP 1: Install Docker Desktop
Postgres is easiest to run as a container instead of installing it directly on your machine. Download Docker Desktop for your OS (docker.com/products/docker-desktop), install it, and make sure it's running (you'll see the whale icon in your taskbar/menu bar).

## STEP 2: Start Postgres with docker-compose
The project's docker-compose.yml already defines a Postgres service with the pgvector extension pre-installed. From the research-assistant/ root folder, first run `cp .env.example .env` and fill in your GROQ_API_KEY. Then run `docker compose up postgres -d` to start just the database in the background.

## STEP 3: Confirm it's running
Run `docker ps` — you should see a container named research_postgres with status 'healthy'. If it's not healthy after ~10 seconds, run `docker compose logs postgres` to see what went wrong (usually a port conflict on 5432).

## STEP 4: Understand the connection string
Postgres is 'connected to' via a URL, not a GUI by default: postgresql+asyncpg://research_user:research_pass@localhost:5432/research_assistant. Breaking it down: research_user/research_pass are the credentials (set in .env), localhost:5432 is where it's listening, and research_assistant is the database name. This exact string is already in your .env as DATABASE_URL — the backend reads it automatically, you don't need to type it anywhere yourself.

## STEP 5 : Create the tables (run the migration)
An empty Postgres database has no tables yet. From backend/, with a Python virtualenv active (`pip install -r requirements.txt`), run `alembic upgrade head`. This reads backend/alembic/versions/0001_initial.py and creates all the tables (research_sessions, papers, paper_chunks, research_gaps, etc.) plus the pgvector extension.

## STEP 6: (Optional) Poke around with a GUI
If you want to see the data visually rather than through the API, install a free tool like TablePlus, DBeaver, or pgAdmin, and create a new connection using the same host/port/user/password/database from step 4. Or, quicker, run `docker exec -it research_postgres psql -U research_user -d research_assistant` to get a command-line SQL prompt straight into the running container.