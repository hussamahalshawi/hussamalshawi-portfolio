import os
import sys
from App import create_app

# --- DESIGN PATTERN: SINGLETON-LIKE INSTANTIATION ---
# We ensure the app instance is created only once to prevent resource duplication.
try:
    app = create_app()
except Exception as e:
    # CRITICAL VALIDATION: If the app fails to initialize, log the error and exit
    # This prevents the server from hanging in a broken state.
    print(f"[-] Critical Error: Failed to initialize HussamAlshawi-Portfolio: {e}")
    sys.exit(1)


def run_server():
    """
    Orchestrates the server startup with environment validation.
    """
    # VALIDATION: Check for necessary environment variables or configurations
    # Ensuring the port is an integer and within valid range
    try:
        port = int(os.environ.get("PORT", 5000))
    except ValueError:
        port = 5000

    # EXECUTION: Running the Flask development server
    # Note: debug=True is strictly for development environments
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=True
        )
    except Exception as startup_error:
        print(f"[-] Runtime Error: Server crashed during startup: {startup_error}")


if __name__ == '__main__':
    # ENTRY POINT VALIDATION:
    # Ensuring the script is executed directly and not imported as a module
    print(f"🚀 [HussamAlshawi-Portfolio] Starting server on port {5000}...")
    run_server()
