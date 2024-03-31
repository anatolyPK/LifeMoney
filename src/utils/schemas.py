from pydantic import BaseModel, conint


class CryptocurrencyListingsValidate(BaseModel):
    limit: conint(gt=0, lt=5000) = 2