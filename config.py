import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configurations
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'academicworld')
} 