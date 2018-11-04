import subprocess

import config
from personal_inventory.presentation import app

if config.ENVIRONMENT == config.Environment.PRODUCTION:
    subprocess.call('gunicorn -b 0.0.0.0 personal_inventory.presentation:app', shell=True)
else:
    app.run()
