import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve API values from .env
API_TOKEN = os.getenv("API_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")

TASK_ID = "api-1"


# Common headers for all test cases
def get_headers(task_id):
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "X-Task-Id": task_id
    }
