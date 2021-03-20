import os

from flask_restx import Api

from serde.models import response_model
from resources.exponea_api.resource import ns


def upgrade_app(app):
    api = Api(app,
              title='Assignment API',
              version='1.0',
              description=f'API specification for {os.environ.get("STAGE", "local")} environment',
              doc='/',
              prefix='/api')

    # Declare serialization/deserialization models
    api.models[response_model.name] = response_model

    # Add namespaces
    api.add_namespace(ns)
