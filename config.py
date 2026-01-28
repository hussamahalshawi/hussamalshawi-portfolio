import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base configuration class. Contains shared settings and
    comprehensive validation logic.
    """
    # 1. Core Security & Identification
    PROJECT_NAME = "HussamAlshawi-Portfolio"
    SECRET_KEY = os.getenv('SECRET_KEY')

    # 2. Path Management (Using Pathlib for modern cross-platform support)
    BASE_DIR = Path(__file__).resolve().parent
    UPLOAD_PATH = BASE_DIR / 'App' / 'static' / 'images'

    # 3. Database Defaults
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'hussam_portfolio')
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')

    @staticmethod
    def validate():
        """
        Validates the presence of critical environment variables.
        Raises ValueError if a required configuration is missing.
        """
        required_vars = {
            'SECRET_KEY': Config.SECRET_KEY,
            'MONGO_DB_NAME': Config.MONGO_DB_NAME
        }

        for var_name, value in required_vars.items():
            if not value:
                # CRITICAL VALIDATION: Halt system if security keys are missing
                raise ValueError(f"[-] Critical Error: {var_name} is not set in the environment.")


class DevelopmentConfig(Config):
    """
    Configuration for Local Development environment.
    """
    DEBUG = True
    # Ensure port is handled as an integer with a safety fallback
    try:
        MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    except (ValueError, TypeError):
        MONGO_PORT = 27017


class ProductionConfig(Config):
    """
    Configuration for Production environment (Server deployment).
    """
    DEBUG = False
    # In production, we typically use a full MongoDB URI
    MONGO_URI = os.getenv('MONGO_URI')


# --- CONFIGURATION FACTORY ---
# Map environment names to their respective config classes
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """
    Returns the appropriate configuration based on the environment variable.
    """
    env = os.getenv('FLASK_ENV', 'development').lower()
    selected_config = config_map.get(env, config_map['default'])

    # Perform integrity check before returning
    selected_config.validate()
    return selected_config