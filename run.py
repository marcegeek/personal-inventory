import os
import subprocess

from personal_inventory.presentation import app

env = os.environ.get('ENV')
if env == 'PROD':
    subprocess.call('gunicorn personal_inventory.presentation:app', shell=True)
else:
    app.run()
