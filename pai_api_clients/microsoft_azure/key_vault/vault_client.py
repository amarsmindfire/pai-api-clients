from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


class AzureKeyVaultClient:
    """
    class to upload and download SFTP
    private key on azure key vault
    """

    def __init__(self, client_id, client_secret, tenant_id, url):
        client_id = client_id
        client_secret = client_secret
        tenant_id = tenant_id

        key_vault_credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        self.secret_client = SecretClient(url, key_vault_credential)

    def upload_key(self, secret_name, key_content):
        try:
            secret = self.secret_client.set_secret(secret_name, key_content)
            response = {secret.name: secret.value}
            return response
        except Exception as e:
            return e

    def download_key(self, secret_name):
        try:
            secret = self.secret_client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            return e
