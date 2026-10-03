from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str = ""


class CustomerOut(CustomerCreate):
    id: int

    model_config = {"from_attributes": True}
