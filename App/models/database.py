from mongoengine import connect, disconnect
import os
import logging
import certifi

# Set up professional logging
logger = logging.getLogger(__name__)


def init_db(app):
    """
    Initializes the MongoDB connection for HussamAlshawi-Portfolio.
    Optimized for dual-environment (Local vs Atlas) with SSL Handshake fix.
    """
    try:
        # 1. Configuration Retrieval
        # We fetch the URI from the environment/config
        db_uri = app.config.get('MONGO_URI')

        # Safety Check: Disconnect any existing alias 'default'
        disconnect(alias='default')

        # 2. Connection Strategy
        if db_uri and ("mongodb+srv" in db_uri or "mongodb://" in db_uri) and "localhost" not in db_uri:
            # PRODUCTION: MongoDB Atlas
            # We enforce tlsCAFile using certifi to override the SSL handshake issue.
            # We also ensure the app name is correctly set.
            connect(
                host=db_uri,
                alias='default',
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )
            print(f"✅ [Database System]: Connected to MongoDB Atlas (Production).")

        else:
            # DEVELOPMENT: Local MongoDB
            db_name = app.config.get('MONGO_DB_NAME', 'hussam_portfolio')
            db_host = app.config.get('MONGO_HOST', 'localhost')

            try:
                db_port = int(app.config.get('MONGO_PORT', 27017))
            except (ValueError, TypeError):
                db_port = 27017

            connect(
                db=db_name,
                host=db_host,
                port=db_port,
                alias='default'
            )
            print(f"✅ [Database System]: Connected to Local MongoDB (Development).")

    except Exception as e:
        # CRITICAL ERROR LOGGING: Capturing specific handshake or timeout failures
        error_msg = f"❌ [Database System Error]: {str(e)}"
        if hasattr(app, 'logger'):
            app.logger.error(error_msg)
        print(error_msg)

        # Halt execution if in production to prevent partial site loading
        if os.environ.get('FLASK_ENV') == 'production':
            raise e