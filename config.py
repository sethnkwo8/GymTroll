import os

from dotenv import load_dotenv

load_dotenv()

TEMPLATES_AUTO_RELOAD = os.environ.get("TEMPLATES_AUTO_RELOAD") #auto reload templates when you refresh
FLASK_DEBUG = os.environ.get("FLASK_DEBUG") #add debugger and for app page to auto save when changes are made
SESSION_PERMANENT = os.environ.get("SESSION_PERMANENT") #session config
SESSION_TYPE = os.environ.get("SESSION_TYPE") #session config
