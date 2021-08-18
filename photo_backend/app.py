# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, request, abort, jsonify
from flask.wrappers import Response
from photo_backend.extensions import (
    cors,
    bcrypt,
    cache,
    db,
    migrate,
)

from photo_backend.api.routes import blueprint as api_blueprint
from photo_backend.auth.routes import blueprint as auth_blueprint


def create_app(config_object="photo_backend.settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)

    @app.errorhandler(404)
    def page_not_found(err):
        return Response(status=404)

    @app.errorhandler(405)
    def page_not_found(err):
        return Response(status=405)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_blueprint)
    return None


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
