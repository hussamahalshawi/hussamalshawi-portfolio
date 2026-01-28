from mongoengine import connect, disconnect
import logging

# Set up professional logging
logger = logging.getLogger(__name__)


def init_db(app):
    """
    Initializes the MongoDB connection using MongoEngine with
    comprehensive validation and error handling.
    """
    try:
        # 1. Safe Configuration Retrieval (Prevents KeyError)
        # We use .get() with default values as a secondary safety net
        db_name = app.config.get('MONGO_DB_NAME', 'hussam_portfolio')
        db_host = app.config.get('MONGO_HOST', 'localhost')
        db_port = app.config.get('MONGO_PORT', 27017)

        # 2. Connection Implementation
        # We ensure any existing connections are closed before opening a new one (Singleton-like behavior)
        disconnect(alias='default')

        connect(
            db=db_name,
            host=db_host,
            port=db_port,
            alias='default'
        )

        # 3. Success Audit Log
        print(f"✅ [Database System]: Successfully connected to MongoDB.")
        print(f"📊 [Status]: DB: {db_name} | Host: {db_host} | Port: {db_port}")

    except Exception as e:
        # CRITICAL VALIDATION: Catch and log the specific failure
        error_msg = f"❌ [Database System Error]: {str(e)}"
        print(error_msg)

        # Log the error for production monitoring
        app.logger.error(error_msg)

        # Strategy: We don't stop the app here to allow the developer to see the
        # dashboard or logs, but in strict production, you might raise SystemExit.