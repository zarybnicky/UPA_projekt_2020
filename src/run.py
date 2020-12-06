from .scrape import main as scrape
from .loader_mongodb import main as load_mongo
from .loader_postgres import main as load_postgres

scrape()
load_mongo()
load_postgres()
