from mongoengine import connect, disconnect
import os
import logging

# Standard library for SSL certificates (Required for MongoDB Atlas)
try:
    import certifi

    ca = certifi.where()
except ImportError:
    ca = None

# Set up professional logging
logger = logging.getLogger(__name__)


def init_db(app):
    """
    HussamAlshawi-Portfolio Database Initializer.
    Connects to MongoDB Atlas (Production) or Localhost (Development)
    based on the available environment configuration.
    """
    try:
        # 1. Fetch the Connection URI from the app config
        # This should be set in Render Environment Variables as MONGO_URLL
        db_uri = app.config.get('MONGO_URI')

        # Robustness: Close any existing connection before starting a new one
        disconnect(alias='default')

        # 2. STRATEGY: Check if we are connecting to Atlas (Production)
        if db_uri and ("mongodb+srv" in db_uri or "mongodb://" in db_uri) and "localhost" not in db_uri:
            # CONNECTION FOR PRODUCTION (Atlas)
            # We use 'tlsCAFile' to solve the SSL Handshake error you encountered.
            connect(
                host=db_uri,
                alias='default',
                tlsCAFile=ca,
                serverSelectionTimeoutMS=5000  # Prevent Gunicorn timeout (5 seconds)
            )
            print(f"✅ [Database System]: Connected to MongoDB Atlas (Production).")

        else:
            # CONNECTION FOR LOCAL DEVELOPMENT
            # Fallback to local settings if no Atlas URI is provided
            db_name = app.config.get('MONGO_DB_NAME', 'hussam_portfolio')
            db_host = app.config.get('MONGO_HOST', 'localhost')

            try:
                db_port = int(app.config.get('MONGO_PORT', 27017))
            except (ValueError, TypeError):
                db_port = 27017

            # Local connections usually don't need SSL/TLS certificates
            connect(
                db=db_name,
                host=db_host,
                port=db_port,
                alias='default'
            )
            print(f"✅ [Database System]: Connected to Local MongoDB (Development).")

    except Exception as e:
        # CRITICAL VALIDATION: Log the specific error for debugging
        error_msg = f"❌ [Database System Error]: {str(e)}"
        if hasattr(app, 'logger'):
            app.logger.error(error_msg)
        print(error_msg)

        # In production, we re-raise the error to stop the app and alert the dev
        if os.environ.get('FLASK_ENV') == 'production':
            raise e