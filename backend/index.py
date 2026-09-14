import sys
import os

# Add the current directory and parent directory to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "app"))

from app.main import app as fastapi_app
from mangum import Mangum

app = Mangum(fastapi_app)