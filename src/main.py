import os
import logging

from flask import Flask
from utils.cors import CORS

from resources.api import upgrade_app

# Set base logging config
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


# Basic Configuration class for an Application
class AppConfig:
    ERROR_404_HELP = False
    RESTX_MASK_SWAGGER = False


app = CORS(Flask(__name__))
app.config.from_object(AppConfig())
upgrade_app(app)

if __name__ == '__main__':
    app.run(debug=not bool(os.getenv('STAGE')), host='0.0.0.0')
