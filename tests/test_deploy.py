import pytest


@pytest.fixture(scope="class", autouse=True)
def vax_passport(VaxPassport, accounts):
    """Deploy VaxPassport contract"""
    contract = VaxPassport.deploy({'from': accounts[0]})
    return contract


class TestContract:
    @staticmethod
    def test_initial_condition(vax_passport, accounts):
        assert vax_passport.owner() == accounts[0].address 
