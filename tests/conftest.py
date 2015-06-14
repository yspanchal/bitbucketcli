from py.path import local
import pytest
import yaml

cfg_files = local().listdir("*.acc_cfg")
ids = [fname.purebasename for fname in cfg_files]


@pytest.fixture(scope="session", params=cfg_files, ids=ids)
def account_cfg(request):
    fname = request.param
    with fname.open() as f:
        return yaml.load(f)


@pytest.fixture(scope="session")
def account(account_cfg):
    return account_cfg["name"]


@pytest.fixture(scope="session")
def repos_cfg(account_cfg):
    return account_cfg["repos"]


@pytest.fixture(scope="session")
def groups_cfg(account_cfg):
    return account_cfg["groups"]


@pytest.fixture(scope="session")
def binbb():
    """bitbucket executable"""
    return local.sysfind("bitbucket")
