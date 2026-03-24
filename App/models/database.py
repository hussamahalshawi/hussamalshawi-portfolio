from mongoengine import connect, disconnect
import logging

# Set up professional logging
logger = logging.getLogger(__name__)


def init_db(app):
    try:
        # 1. محاولة جلب رابط Atlas أولاً
        db_uri = app.config.get('MONGO_URI')

        disconnect(alias='default')

        if db_uri and "mongodb+srv" in db_uri:
            # الاتصال عبر الرابط الكامل (Atlas)
            connect(host=db_uri, alias='default')
            print(f"✅ [Database System]: Connected to MongoDB Atlas.")
        else:
            # الاتصال المحلي التقليدي
            db_name = app.config.get('MONGO_DB_NAME', 'hussam_portfolio')
            db_host = app.config.get('MONGO_HOST', 'localhost')
            db_port = app.config.get('MONGO_PORT', 27017)
            connect(db=db_name, host=db_host, port=db_port, alias='default')
            print(f"✅ [Database System]: Connected to Local MongoDB.")

    except Exception as e:
        error_msg = f"❌ [Database System Error]: {str(e)}"
        app.logger.error(error_msg)
        print(error_msg)