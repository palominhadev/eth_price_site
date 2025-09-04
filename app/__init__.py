from flask import Flask


def create_app():
    app = Flask(__name__)

    '''
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('settings.Config')
    '''

    from .views import views
    app.register_blueprint(views)

    return app
