import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app, db
from app.models import User, Assignment, Notice, Class, UserPreferences

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Assignment=Assignment, Notice=Notice, Class=Class, UserPreferences=UserPreferences)


if __name__ == '__main__':
    app.run()
