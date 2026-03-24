from mongoengine import connect, disconnect
import os
import certifi

def init_db(app):
    """
    Final Database configuration for HussamAlshawi-Portfolio.
    Target Database: HussamPortfolio
    """
    try:
        # جلب الرابط من الإعدادات
        db_uri = app.config.get('MONGO_URI')
        # اسم القاعدة الموحد للجهتين
        target_db = "HussamPortfolio"

        disconnect(alias='default')

        if db_uri and "mongodb+srv" in db_uri:
            # الاتصال بالسيرفر (Atlas)
            # ملاحظة: إذا كان الاسم موجوداً في الرابط فسيستخدمه،
            # وإذا لم يكن، سنحدده هنا لضمان الدقة.
            connect(
                host=db_uri,
                db=target_db,
                alias='default',
                tlsCAFile=certifi.where(),
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=10000
            )
            app.logger.info(f"✅ [Database]: Connected to Atlas Database: {target_db}")
        else:
            # الاتصال المحلي (Local)
            connect(
                db=target_db,
                host='localhost',
                port=27017,
                alias='default'
            )
            print(f"🏠 [Database]: Connected to Local Database: {target_db}")

    except Exception as e:
        error_msg = f"❌ [Database Error]: {str(e)}"
        if hasattr(app, 'logger'):
            app.logger.error(error_msg)
        print(error_msg)