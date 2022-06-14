import brownie
import pytest

# --------------- ACCOUNT ROLES --------------- #
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
def disallowed_account(accounts):
    return accounts[3]

@pytest.fixture(scope="session", autouse=True)
def vaccinated_passports(accounts):
    return accounts[4:6]

@pytest.fixture(scope="session", autouse=True)
def unvaccinated_passports(accounts):
    return accounts[6:8]

@pytest.fixture(scope="session", autouse=True)
def not_owner(accounts):
    return accounts[8]

@pytest.fixture(scope="session", autouse=True)
def generic_account(accounts):
    return accounts[9]

# ----------------- PASSPORT ------------------ #
@pytest.fixture(scope="session", autouse=True)
def vax_passport(VaxPassport, contract_owner):
    contract = VaxPassport.deploy({'from': contract_owner})
    return contract


class TestDeploy:
    @staticmethod
    def test_initial_condition(vax_passport, contract_owner):
        # contract owner is correctly set and has write access
        assert vax_passport.owner() == contract_owner.address
        assert vax_passport.access(contract_owner.address)['allowed'] is True


class TestGrantAccess:
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

class TestRevokeAccess:
    @staticmethod
    def test_not_owner_revoke_access(vax_passport, not_owner, revoked_account):
        # someone who is not the contract owner is trying to revoke someone else's access
        with brownie.reverts("Only contract's owner is allowed to revoke write access"):
            vax_passport.revoke_access(revoked_account.address, { 'from': not_owner })

    @staticmethod
    def test_owner_revoke_access(vax_passport, contract_owner, revoked_account):
        # contract owner is trying to revoke someone's access
        vax_passport.revoke_access(revoked_account.address, { 'from': contract_owner })

class TestAddDose:
    @staticmethod
    def test_granted_access_add_dose(vax_passport, granted_account, vaccinated_passports):
        # account with 'write access' is trying to add dose to someone
        vax_passport.add_dose(vaccinated_passports[0].address, 123456, 123, { 'from': granted_account } )
        assert vax_passport.passports(vaccinated_passports[0].address)['id'] == 123456
        assert len(vax_passport.passports(vaccinated_passports[0].address)['doses']) > 0

    @staticmethod
    def test_disallowed_add_dose(vax_passport, disallowed_account, vaccinated_passports):
        # account with no 'write access' is trying to add dose to someone
        with brownie.reverts("You need 'write access' to be able to add dose"):
            vax_passport.add_dose(vaccinated_passports[0].address, 123456, 123, { 'from': disallowed_account } )
    
    @staticmethod
    def test_revoked_add_dose(vax_passport, revoked_account, vaccinated_passports):
        # account with revoked 'write access' is trying to add dose to someone
        with brownie.reverts("You need 'write access' to be able to add dose"):
            vax_passport.add_dose(vaccinated_passports[0].address, 123456, 123, { 'from': revoked_account } )
    
    @staticmethod
    def test_wrong_passport_id(vax_passport, granted_account, vaccinated_passports):
        # account with 'write access' is trying to add a second dose to someone,
        # but the passport.id is wrong: 123456 != 123457
        with brownie.reverts("Inconsistent passport id"):
            vax_passport.add_dose(vaccinated_passports[0].address, 123457, 123, { 'from': granted_account } )


class TestViewPassport:
    @staticmethod
    def test_view_vaccinated_passport(vax_passport, generic_account, vaccinated_passports):
        # some generic account is trying to read the vaccination status of a
        # vaccinated_passport
        passport = vax_passport.view_passport(vaccinated_passports[0].address, {'from': generic_account })
        assert passport['id'] == 123456
        assert len(passport['doses']) > 0

    @staticmethod
    def test_view_unvaccinated_passport(vax_passport, generic_account, unvaccinated_passports):
        # some generic account is trying to read the vaccination status of a
        # unvaccinated_passport
        passport = vax_passport.view_passport(unvaccinated_passports[0].address, {'from': generic_account })
        assert passport['id'] == 0
        assert len(passport['doses']) == 0