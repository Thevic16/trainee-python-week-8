from models.models import AccountModel
from werkzeug.security import safe_str_cmp

from utilities.logger import Logger


def authenticate(email, password):
    Logger.debug(f'email:{email}')
    Logger.debug(f'email:{password}')
    account = AccountModel.find_by_email(email)
    if account and safe_str_cmp(account.password, password):
        return account


def identity(payload):
    account_id = payload['identity']
    Logger.debug(f'account_id:{account_id}')
    return AccountModel.find_by_id(account_id)
