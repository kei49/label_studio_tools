import pandas as pd
import urllib.parse
from datetime import datetime

from label_studio_tools.config import Config

from label_studio_tools.azure_blob_storage import ABSClient


class Main:
    def __init__(self, csv_name: str) -> None:
        config = Config()
        self.azure_storage_connection_string = config.AZURE_STORAGE_CONNECTION_STRING
        self.azure_storage_container_name = config.AZURE_STORAGE_CONTAINER_NAME
        self.azure_storage_account_name = config.AZURE_STORAGE_ACCOUNT_NAME
        self.import_csv_root_path = config.IMPORT_CSV_ROOT_PATH
        self.export_audio_path = config.EXPORT_AUDIO_ROOT_PATH

        print(config)

    def download_all_audio_files_by_csv(self, csv_name: str):
        csv_path = f"{self.import_csv_root_path}/{csv_name}"
        df = self.load_csv(csv_path)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        for _, row in df.iterrows():
            azure_blob_path = row["azure_blob_path"]
            file_extension = azure_blob_path.split(".")[-1]
            audio_id = row["id"]
            destination_file_name = f"{self.export_audio_path}/{timestamp}-{csv_name}/{audio_id}.{file_extension}"

            print(f"Downloading {azure_blob_path=} to {destination_file_name=}")

            abs_client = ABSClient(
                self.azure_storage_connection_string, self.azure_storage_container_name
            )
            abs_client.download_blob_file(azure_blob_path, destination_file_name)

    def load_csv(self, path: str):
        df = pd.read_csv(path, escapechar=None)
        df["azure_blob_path"] = df["audio"].apply(self.convert_audio_str_to_abs_path)
        return df

    def convert_audio_str_to_abs_path(self, audio_str: str):
        audio_path = urllib.parse.unquote(audio_str)
        azureb_blob_storage_path = f"https://{self.azure_storage_account_name}.blob.core.windows.net/{audio_path.split('//')[1]}"
        return azureb_blob_storage_path


if __name__ == "__main__":
    # Place the csv inside ./data/import
    csv_name = "CSV_FILE_EXPORTED_FROM_LABEL_STUDIO.csv"

    main = Main(csv_name)
    main.download_all_audio_files_by_csv(csv_name)
