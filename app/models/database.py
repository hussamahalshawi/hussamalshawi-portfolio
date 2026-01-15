from mongoengine import connect

def init_db(app):
    try:
        connect(
            db=app.config['MONGO_DB_NAME'],
            host=app.config['MONGO_HOST'],
            port=app.config['MONGO_PORT']
        )
        print(f"✅ تم الاتصال بنجاح بـ MongoDB: {app.config['MONGO_DB_NAME']}")
    except Exception as e:
        print(f"❌ فشل الاتصال بقاعدة البيانات: {e}")