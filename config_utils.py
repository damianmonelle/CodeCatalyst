
import os
import logging

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def verify_environment_variables(required_env_vars):
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        logging.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False, missing_vars
    logging.info("All required environment variables are set.")
    return True, None
