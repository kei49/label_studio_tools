import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(".env")


@dataclass
class Config:
    AZURE_STORAGE_CONNECTION_STRING: str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    AZURE_STORAGE_ACCOUNT_NAME: str = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
    AZURE_STORAGE_CONTAINER_NAME: str = os.environ["AZURE_STORAGE_CONTAINER_NAME"]
    IMPORT_CSV_ROOT_PATH: str = "data/import"
    EXPORT_AUDIO_ROOT_PATH: str = "data/export"
