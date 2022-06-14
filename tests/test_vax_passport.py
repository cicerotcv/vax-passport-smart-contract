import brownie
import pytest


@pytest.fixture(scope="session", autouse=True)
def contract_owner(accounts):
    return accounts[0]

@pytest.fixture(scope="session", autouse=True)
def granted_account(accounts):
    return accounts[1]

@pytest.fixture(scope="session", autouse=True)
def revoked_account(accounts):
    return accounts[2]

@pytest.fixture(scope="session", autouse=True)
def not_owner(accounts):
    return accounts[8]

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
        # contract owner is correctly set and has write access
        assert vax_passport.owner() == contract_owner.address
        assert vax_passport.access(contract_owner.address)['allowed'] is True


class TestContractGrantAccess:
    @staticmethod
    def test_not_owner_grant_access(vax_passport, not_owner, generic_account):
        # someone who is not the contract owner is trying to give write access to some
        # generic account
        with brownie.reverts("Only contract's owner is allowed to grant write access"):
            vax_passport.grant_access(not_owner.address, "BRA", {'from': generic_account})

    @staticmethod
    def test_owner_grant_access(vax_passport, contract_owner, granted_account, revoked_account):
        # contract owner is trying to give write access to some allowed account
        vax_passport.grant_access(granted_account.address, "BRA", { 'from': contract_owner })
        vax_passport.grant_access(revoked_account.address, "ALB", { 'from': contract_owner })

class TestContractRevokeAccess:
    @staticmethod
    def test_not_owner_revoke_access(vax_passport, not_owner, revoked_account):
        # someone who is not the contract owner is trying to revoke someone else's access
        with brownie.reverts("Only contract's owner is allowed to revoke write access"):
            vax_passport.revoke_access(revoked_account.address, { 'from': not_owner })

    @staticmethod
    def test_owner_revoke_access(vax_passport, contract_owner, revoked_account):
        # contract owner is trying to revoke someone's access
        vax_passport.revoke_access(revoked_account.address, { 'from': contract_owner })
