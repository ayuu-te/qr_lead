from app import app as flask_app

# Required handler for Vercel
def handler(environ, start_response):
    return flask_app(environ, start_response)
