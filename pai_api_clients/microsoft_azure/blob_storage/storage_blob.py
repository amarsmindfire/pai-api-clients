import base64
from datetime import datetime, timedelta
import os

from azure.storage.blob import BlobServiceClient, BlobClient, BlobSasPermissions, generate_blob_sas


class AzureStorageBlob:
    def __init__(self, storage_conn_string, storage_name, storage_conn_key, container_name):
        self.connect_str = storage_conn_string
        self.connect_key = storage_conn_key

        # Create the BlobServiceClient object which will be used to create a container client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connect_str)

        self.storage_name = storage_name
        # Create a unique name for the container
        self.container_name = container_name

        self.container_client = None

    def get_container_client(self):
        """
        get blob container object
        :return:
        """
        try:
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
        except Exception as e:
            print('Exception in get_container_Client', e)

    def get_blob(self, blob_name):
        """
        List the blobs in the container
        :return:
        """
        print(self.container_name, blob_name)
        try:
            blob_client = BlobClient.from_connection_string(
                conn_str=self.connect_str, container_name=self.container_name, blob_name=blob_name
            )
            with open(f'mro.tiff', "wb") as my_blob:
                blob_data = blob_client.download_blob()
                blob_data.readinto(my_blob)

            encoded_string = None
            with open("mro.tiff", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            os.remove('mro.tiff')
            return encoded_string
        except Exception as e:
            print('Exception in get blob', e)

    def handle_blob(self, query_string):
        """
        get base64 encoded string for each image
        :param query_string:
        :return: encoded_string_list
        """
        # encoded_string_list = []
        sas_tokens = []
        self.get_container_client()
        for request_form_files in query_string:
            sas_token = self.get_blob_sas_token(request_form_files.file_name)
            sas_tokens.append(sas_token)
            # encoded_string = self.get_blob(request_form_files.file_name)
            # encoded_string_list.append(encoded_string.decode("utf-8"))
        return sas_tokens

    def get_blob_sas_token(self, blob_name):
        try:
            name = blob_name.split('.')[0]
            page_index = int(name.split('-')[-1]) if name else None
        except Exception as e:
            print(e)
            page_index = None
        expiry = datetime.utcnow() + timedelta(hours=10)

        sas_token = generate_blob_sas(
            account_name=self.storage_name,
            container_name=self.container_name,
            blob_name=blob_name,
            account_key=self.connect_key,
            permission=BlobSasPermissions(read=True),
            expiry=expiry)

        sas_url_with_page_index = {
            'page_number': page_index,
            'page_image_url': f"https://{self.storage_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_token}"

        }
        return sas_url_with_page_index
