# @version ^0.3.2
# VaxPassport v0.0.1


# ------------- Struct Definitions ------------- #

# Struct defining management access
struct WriteAccess:
  allowed: bool
  countryCode: String[3]  # https://www.iso.org/obp/ui/#search

# Struct defining vaccination data
struct VaxPassport:
  id: uint128 # person id (CPF, RG etc.)
  doses: DynArray[int32, 30]

# Official institution address (e.g. OMS)
owner: public(address)

# Addresses allowed to write data to contract
access: public(HashMap[address, WriteAccess])

# Addresses related vaccination passports
passports: public(HashMap[address, VaxPassport])


# ------------- Internal useful methods ------------- #

# ------------- External methods ------------- #

@external
def __init__():
  self.owner = msg.sender                 # define contract's owner
  self.access[msg.sender].allowed = True  # grant access to contract's owner
