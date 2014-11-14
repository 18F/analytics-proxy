from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from analytics_proxy import app, db ,load_data
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def initalize_database():
    with open('analytics_urls.txt') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip("\n").split("|")
        load_data(endpoint=line[0], url=line[1])

if __name__ == '__main__':
    manager.run()
