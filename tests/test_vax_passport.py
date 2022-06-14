import brownie
import pytest


@pytest.fixture(scope="session", autouse=True)
def contract_owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session", autouse=True)
def allowed_account(accounts):
    return accounts[1]


@pytest.fixture(scope="session", autouse=True)
def disallowed_account(accounts):
    return accounts[2]


@pytest.fixture(scope="session", autouse=True)
def generic_account(accounts):
    return accounts[9]


@pytest.fixture(scope="session", autouse=True)
def vax_passport(VaxPassport, contract_owner):
    contract = VaxPassport.deploy({'from': contract_owner})
    return contract


class TestContractDeploy:
    @staticmethod
    def test_initial_condition(vax_passport, contract_owner):
        assert vax_passport.owner() == contract_owner.address
        assert vax_passport.access(contract_owner.address)['allowed'] is True
