import os

from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.getcwd(), ".env")
a = load_dotenv(override=True)

# def load_environment_variables(env_file_path):
#     with open(env_file_path, 'r') as file:
#         for line in file:
#             if line.strip() != '' and not line.startswith('#'):
#                 key, value = line.strip().split(' ', 1)
#                 # print (key,value)
#                 os.environ[key] = value

# load_environment_variables('./.env')

def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise ValueError(f'Environment variable {key} not found')
    return value