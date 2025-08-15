"""Users: Serialiser for User Model."""

from uuid import UUID
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, field_validator, validate_call

from config import AppConfig
from lib.interfaces.exceptions import UserError
from lib.utils.constants.users import Regex, Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.user.users import User
from serialisers.serialiser import BaseSerialiser


class CreateUserData(BaseModel):
    """Data Model for User Creation."""

    email: str
    password: str

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        """Validate User Email."""

        if not Regex.EMAIL.value.match(value):
            raise UserError("Invalid Email.")

        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Validate User Password."""

        if not Regex.PASSWORD.value.match(value):
            raise UserError("Invalid Password.")

        return value


class UpdateUserData(BaseModel):
    """Data Model for User Update."""

    status: Status | None = None
    password: str | None = None

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate User Status."""

        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise UserError("Invalid Status.")

        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Validate User Password."""

        if not Regex.PASSWORD.value.match(value):
            raise UserError("Invalid Password.")

        return value


class UserSerialiser(User, BaseSerialiser):
    """Serialiser for the User Model."""

    @validate_call
    def get_user(self, user_id: str) -> str:
        """CRUD Operation: Read User."""

        with Session(ENGINE) as session:
            query = select(User).filter(User.user_id == user_id)
            user = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserError("User Not Found.")

            return self.__get_encrypted_model_data__(user)

    @validate_call
    def create_user(self, data: CreateUserData) -> str:
        """CRUD Operation: Create User."""

        with Session(ENGINE) as session:
            self.email = str(self.__get_valid_email__(data.email))
            self.password = str(
                self.__get_valid_password__(data.password, str(self.salt_value))
            )
            self.user_id = str(
                self.__get_valid_user_id__(str(data.email), data.password)
            )

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User Not created. Already exists.") from exc

            return str(self)

    @validate_call
    def update_user(
        self,
        private_id: str,
        data: UpdateUserData,
    ) -> str:
        """CRUD Operation: Update User."""

        with Session(ENGINE) as session:
            user = session.get(User, private_id)

            if user is None:
                raise UserError("User Not Found.")

            if data.password:
                valid_password = self.__get_valid_password__(
                    data.password, str(user.salt_value)
                )
                valid_user_id = self.__get_valid_user_id__(
                    str(decrypt_data(str(user.email))), data.password
                )
                setattr(user, "password", valid_password)
                setattr(user, "user_id", valid_user_id)

            if data.status:
                setattr(user, "status", data.status)

            try:
                session.add(user)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User not Updated.") from exc

            return str(user)

    @validate_call
    def delete_user(self, private_id: UUID) -> str:
        """CRUD Operation: Delete User."""

        with Session(ENGINE) as session:
            user = session.get(User, private_id)

            if not user:
                raise UserError("User Not Found")

            try:
                session.delete(user)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_valid_email__(self, email: str) -> str:
        """Get Valid Email."""

        return encrypt_data(email.encode())

    def __get_valid_password__(self, password: str, salt_value: str) -> str:
        """Get Valid Password."""

        return str(get_hash_value(password, str(salt_value)))

    def __get_valid_user_id__(self, email: str, password: str) -> str:
        """Get Valid User ID."""

        return get_hash_value(str(email) + password, str(AppConfig().salt_value))
