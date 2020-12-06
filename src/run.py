import sys; sys.path.insert(0, '.')

from scrape import main as scrape
from loader_mongodb import main as load_mongo
from loader_postgres import main as load_postgres
from tasks import task_A, task_B, task_C

scrape()
load_mongo()
load_postgres()
task_A()
task_B()
task_C()
