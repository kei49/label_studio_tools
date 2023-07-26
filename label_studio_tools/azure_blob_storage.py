import os
from datetime import datetime, timedelta
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
    BlobClient,
)

from label_studio_tools.utils import setup_dir_for_file_path


class ABSClient:
    def __init__(self, connection_string: str, container_name: str) -> None:
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_name = container_name

    def download_blob_file(self, blob_path: str, dest_path: str) -> None:
        setup_dir_for_file_path(dest_path)

        sas_url = self._create_sas_url(blob_path)
        blob_client = BlobClient.from_blob_url(sas_url)

        with open(dest_path, "wb") as download_file:
            data = blob_client.download_blob().readall()
            download_file.write(data)

            print(f"Downloaded to {dest_path=}")

    def _create_sas_url(self, blob_path: str) -> str:
        blob_name = blob_path.split(f"{self.container_name}/")[-1]
        sas_token = generate_blob_sas(
            self.blob_service_client.account_name,
            container_name=self.container_name,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=10),
        )

        sas_url = f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"
        return sas_url
