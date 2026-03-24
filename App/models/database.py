from mongoengine import connect, disconnect
import os
import certifi
import ssl # أضفنا هذا الاستيراد

def init_db(app):
    try:
        db_uri = app.config.get('MONGO_URI')
        disconnect(alias='default')

        if db_uri and "mongodb+srv" in db_uri:
            # PRODUCTION: الاتصال بـ Atlas
            # سنقوم هنا بتعطيل التحقق الصارم من الشهادات لضمان عمل المصافحة (Handshake)
            connect(
                host=db_uri,
                alias='default',
                tls=True,
                tlsCAFile=certifi.where(),
                tlsAllowInvalidCertificates=True, # هامة جداً لتجاوز خطأ SSL في Render
                serverSelectionTimeoutMS=10000,   # زيادة المهلة لـ 10 ثوانٍ
                connectTimeoutMS=10000
            )
            print(f"✅ [Database System]: Connected to Atlas (SSL Bypass Mode).")
        else:
            # DEVELOPMENT: الاتصال المحلي
            db_name = app.config.get('MONGO_DB_NAME', 'hussam_portfolio')
            connect(db=db_name, host='localhost', port=27017, alias='default')
            print(f"✅ [Database System]: Connected to Local MongoDB.")

    except Exception as e:
        print(f"❌ [Database System Error]: {str(e)}")
        if os.environ.get('FLASK_ENV') == 'production':
            raise e