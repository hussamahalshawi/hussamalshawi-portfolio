import os
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base configuration class. Contains shared settings, Cloudinary integration,
    and comprehensive validation logic.
    """
    # 1. Core Security & Identification
    PROJECT_NAME = "HussamAlshawi-Portfolio"
    SECRET_KEY = os.getenv('SECRET_KEY')

    # 2. Cloudinary Configuration (The New Integration)
    # These values should be set in your .env locally and Render Dashboard in production
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    # 3. Path Management (Legacy/Local - Keep if you still need local storage for other things)
    BASE_DIR = Path(__file__).resolve().parent
    UPLOAD_PATH = BASE_DIR / 'App' / 'static' / 'images'
    UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

    # 4. Database Defaults
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'hussam_portfolio')
    MONGO_URI = os.getenv('MONGO_URLL')

    @staticmethod
    def validate():
        """
        Validates the presence of critical environment variables.
        Ensures Cloudinary and Secret keys are present before starting.
        """
        critical_vars = {
            "SECRET_KEY": Config.SECRET_KEY,
            "CLOUDINARY_CLOUD_NAME": Config.CLOUDINARY_CLOUD_NAME,
            "CLOUDINARY_API_KEY": Config.CLOUDINARY_API_KEY,
            "CLOUDINARY_API_SECRET": Config.CLOUDINARY_API_SECRET
        }

        for var_name, value in critical_vars.items():
            if not value:
                raise ValueError(f"[-] Critical Error: {var_name} is not set in environment variables.")

    @staticmethod
    def init_cloudinary():
        """
        Initializes the Cloudinary SDK and prints confirmation to Terminal.
        """
        cloudinary.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET,
            secure=True
        )
        print(f"☁️  [Cloudinary]: SDK Initialized for cloud: {Config.CLOUDINARY_CLOUD_NAME}")

class DevelopmentConfig(Config):
    """
    Configuration for Local Development environment.
    """
    DEBUG = True
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))


class ProductionConfig(Config):
    """
    Configuration for Production environment (Server deployment).
    """
    DEBUG = False
    # In production, we typically use a full MongoDB URI
    pass


# --- CONFIGURATION FACTORY ---
# Map environment names to their respective config classes
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """
    Returns the appropriate configuration and initializes cloud services.
    """
    env = os.getenv('FLASK_ENV', 'development').lower()
    selected_config = config_map.get(env, config_map['default'])

    # Perform integrity check
    selected_config.validate()

    # Initialize Cloudinary SDK
    selected_config.init_cloudinary()

    return selected_config