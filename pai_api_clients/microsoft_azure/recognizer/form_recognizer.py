import json
import os
from pathlib import Path
import time
from requests import get, post

from azure.ai.formrecognizer import FormRecognizerClient, FormTrainingClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import ContainerClient

from .constants import APPLICATION_TYPE, CONN_URL, SCHEMA, TMP_LABEL_LIST


class AzureFormRecognizer:
    """
    Class helps to handle form recognition easily.
    1. Extract Form Layout
    2. Train a custom model SAS url containing at least 5 files(pdf, .ocr.json, .labels.json)
    3. helps to create a label file for training.
    4. Upload files to blob container
    5. download files from blob using blob name and some credentials
    """
    def __init__(self, endpoint, key, conn=None):
        self.key = key
        self.form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
        self.form_training_client = FormTrainingClient(endpoint, AzureKeyCredential(key))
        self.conn = CONN_URL if not conn else conn
        self.url = f'https://{self.conn}/formrecognizer/v2.1/layout/analyze'

    def extract_form_layout(self, doc_path, output_dir, file_type='PDF'):
        headers = {
            # Request headers
            'Content-Type': APPLICATION_TYPE[file_type],
            'Ocp-Apim-Subscription-Key': self.key,
        }

        try:
            _, filename = os.path.split(doc_path)

            if os.path.isdir(output_dir):
                output_path = os.path.join(output_dir, f'{filename}.ocr.json')
            else:
                raise Exception("Output directory doesn't exits...")

            with open(doc_path, "rb") as fd:
                form_data = fd.read()
            if not form_data:
                raise Exception(f"Empty Doc {doc_path}")

            response = post(url=self.url, data=form_data, headers=headers)

            if response.status_code != 202:
                raise Exception("Failed to submit request...")

            print(f"POST analyze succeeded. Response URL: {response.headers['Operation-Location']}")
            get_url = response.headers["operation-location"]

            return self.fetch_response(get_url, output_path)
        except Exception as e:
            print(e)

    def fetch_response(self, get_url, output_path):
        n_tries = 10
        n_try = 1
        wait_sec = 2
        headers = {"Ocp-Apim-Subscription-Key": self.key}

        while n_try <= n_tries:
            try:
                print(f"Fetching submitted result trial {n_try}")
                resp = get(url=get_url, headers=headers)
                resp_json = resp.json()

                if resp.status_code != 200:
                    print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                    return

                status = resp_json["status"]
                if status == "succeeded":
                    out_file = open(output_path, "w")
                    json.dump(resp_json, out_file, indent=6)
                    out_file.close()
                    print(f"Analysis succeeded. Saved at {output_path}")
                    return output_path

                if status == "failed":
                    print("Analysis failed....")
                    return
                time.sleep(wait_sec)
                n_try += 1
            except Exception as e:
                print(f"GET analyze results failed: {str(e)}")
                return
        print("Analyze operation did not complete within the allocated time.")

    def train_model(self, sas_url, model_name):
        model = None
        try:
            poller = self.form_training_client.begin_training(
                sas_url, use_training_labels=True, model_name=model_name
            )
            model = poller.result()
            if model.status == "succeeded":
                print(f"Model({model.model_name}) created successfully. Model ID: {model.model_id}")
        except Exception as e:
            print(f"Some error occurred while creating model '{model_name}'", e)
        return model

    def extract_form_using_custom_model(self, model_id, doc_path):
        try:
            with open(doc_path, "rb") as fd:
                form = fd.read()

            if not form:
                raise Exception(f"Empty Doc {doc_path}")

            poller = self.form_recognizer_client.begin_recognize_custom_forms(model_id=model_id, form=form)
            form_layout = poller
            return form_layout

        except Exception as e:
            raise Exception(f"failed to open: {doc_path}", e)

    def create_label_file(self, output_dir, doc_name, label_list=TMP_LABEL_LIST, labeling_state=2):
        try:
            if os.path.isdir(output_dir):
                output_path = os.path.join(output_dir, f'{doc_name}.labels.json')
            else:
                raise Exception("Output directory doesn't exits...")

            data = {
                "$schema": SCHEMA, "document": doc_name, "labels": label_list, "labelingState": labeling_state
            }
            out_file = open(output_path, "w")
            json.dump(data, out_file, indent=6)
            out_file.close()
            print(f"Successfully created. File loc: {output_path}")
        except Exception as e:
            print("failed to create File. ", e)

    def upload_files_to_blob_container(self, conn_string, container_name, file_paths, folder_path=""):
        container_client = ContainerClient.from_connection_string(conn_str=conn_string, container_name=container_name)
        for file in file_paths:
            _, filename = os.path.split(file)
            if os.path.isfile(file) and not file.startswith('.'):
                blob_client = container_client.get_blob_client(os.path.join(folder_path, filename))

                with open(file, "rb") as data:
                    blob_client.upload_blob(data)
                    print(f"{filename} Uploaded..")
            else:
                print(f"{filename} is not a file...")

    def download_blob(self, conn_string, container_name, blob_name, output_path=''):
        """
        Download blob file from azure container

        :param conn_string:
        :param container_name:
        :param blob_name:
        :param output_path:
        :return:
        """
        container_client = ContainerClient.from_connection_string(
            conn_str=conn_string,
            container_name=container_name
        )
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob()

        if not blob_data:
            return False

        output_path = os.path.join(output_path, os.path.split(blob_name)[0])
        Path(output_path).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(output_path, os.path.basename(blob_name))

        with open(file_path, "wb") as my_blob:
            blob_data.readinto(my_blob)

        return file_path
