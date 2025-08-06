from app import app
from app.db_init import init_db_command

app.cli.add_command(init_db_command)

if __name__ == "__main__":
    # Run with: flask --app run.py init-db  (to initialize database for first use)
    app.run()
