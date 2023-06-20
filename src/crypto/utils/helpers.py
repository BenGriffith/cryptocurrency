from google.oauth2 import service_account

def service_credentials(service_acct: dict):
    return service_account.Credentials.from_service_account_file(service_acct)