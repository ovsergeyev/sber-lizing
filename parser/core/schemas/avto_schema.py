from typing import Optional

from pydantic import BaseModel, validator


class AutoSchema(BaseModel):
    auto_id: int
    image_url: str
    title: str
    brand: Optional[str] = None
    model: Optional[str] = None
    vin: Optional[str] = None
    year_of_release: Optional[int] = None
    mileage: Optional[int] = None
    location: str
    price: int
    old_price: Optional[int] = None
    min_installment: Optional[int] = None
    link: str

    @validator("price", pre=True)
    def parse_price(cls, v):
        if isinstance(v, str):
            res = v.replace("от", "")
            res = res.replace("₽", "")
            res = "".join(res.split())
            return int(res)
        return v

    @validator("min_installment", pre=True)
    def parse_min_installment(cls, v):
        if isinstance(v, str):
            res = v.replace("от", "")
            res = res.replace("₽", "")
            res = "".join(res.split())
            return int(res)
        return v

    @validator("mileage", pre=True)
    def parse_mileage(cls, v):
        if isinstance(v, str):
            try:
                res = "".join(v.split())
                return int(res)
            except:
                return -1
        return v
