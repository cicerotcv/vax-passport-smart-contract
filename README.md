# Vaccination Passport Smart Contract


### 


### Testing

Start ganache development server. Manually deploying like this makes it easier to run tests

```shell
$ ganache-cli --port 8545 --gasLimit 12000000 --accounts 10 --hardfork istanbul --mnemonic brownie
```

Run tests
```
$ brownie test  -v --no-header
```