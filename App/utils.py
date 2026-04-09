import cloudinary.uploader
import logging
import sys

# --- Improved Logging Setup ---
# This configuration ensures logs go to BOTH the file and the console (Terminal)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Catch everything

# Create handlers
file_handler = logging.FileHandler('media_errors.log')
stream_handler = logging.StreamHandler(sys.stdout)  # This brings back Terminal logs

# Create format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to logger
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def upload_media_to_cloud(file_stream, folder_name="profile"):
    """
    Uploads a file to Cloudinary with detailed console debugging.
    """
    try:
        # Debug: Check if file object exists
        if not file_stream:
            print("🔍 [Cloudinary Debug]: No file object received at all.")
            return None

        if file_stream.filename == '':
            print("🔍 [Cloudinary Debug]: File object exists but filename is empty.")
            return None

        print(f"🚀 [Cloudinary Debug]: Attempting to upload: {file_stream.filename}")

        # Upload process
        upload_result = cloudinary.uploader.upload(
            file_stream,
            folder=f"HussamAlshawi-Portfolio/{folder_name}",
            resource_type="image"
        )

        secure_url = upload_result.get("secure_url")
        print(f"✅ [Cloudinary Debug]: Upload Successful! URL: {secure_url}")

        return secure_url

    except Exception as e:
        # Detailed error log
        logger.error(f"❌ Cloudinary Upload Failed: {str(e)}")
        print(f"❌ [Cloudinary Debug]: Critical Exception: {str(e)}")
        return None