from app.main import apps
from mangum import Mangum

handler = Mangum(app)s