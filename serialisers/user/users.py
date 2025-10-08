"""Users: Serialiser for User Model."""

from typing import cast
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from pydantic import validate_call

<<<<<<< HEAD
from config import AppConfig
from lib.exceptions import UserError
from lib.types.user import UserUpdateData
from lib.utils.constants.users import Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
=======
from lib.interfaces.exceptions import UserError
from lib.interfaces.user.users import CreateUserData, UpdateUserData
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.user.users import User
from serialisers.serialiser import ISerialiser


class UserSerialiser(ISerialiser):
    """Serialiser for the User Model."""

<<<<<<< HEAD
    __SERIALISER_EXCEPTION__ = UserError

    def get_user(self, user_id: str) -> str:
        """CRUD Operation: Read User."""

        with Session(ENGINE) as session:
            query = select(User).filter(cast(User.user_id, String) == user_id)
            user = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserError("User Not Found.")

            return self.__get_encrypted_model_data__(user)

    def create_user(self, email: str, password: str) -> str:
        """CRUD Operation: Create User."""

        with Session(ENGINE) as session:
            self.email = str(self.__get_valid_email__(email))
            self.password = str(
                self.__get_valid_password__(password, str(self.salt_value))
            )
            self.user_id = str(self.__get_valid_user_id__(str(email), password))

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User Not created.") from exc

            return str(self)

    def update_user(self, private_id: UUID, data: UserUpdateData) -> str:
        """CRUD OperatiFon: Update User."""

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
=======
    @validate_call
    def create(self, data: CreateUserData) -> User:
        """CRUD Operation: Create User."""

        with Session(ENGINE) as session:
            salt_value = uuid4()
            password = get_hash_value(data.password, str(salt_value))
            user = User(email=data.email, password=password, salt_value=salt_value)
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9

            try:
                session.add(user)
                session.commit()
                session.refresh(user)
            except IntegrityError as exc:
                raise UserError("User Not created. Already exists.") from exc

            return user

    @validate_call
    def read(self, model_id: UUID) -> User:
        """CRUD Operation: Read User."""

        with Session(ENGINE) as session:
            user = (
                session.query(User)
                .options(joinedload(User.login_history))
                .get(model_id)
            )

            if not user:
                raise UserError("User Not Found.")

            return user

    @validate_call
    def update(self, model_id: UUID, data: UpdateUserData) -> User:
        """CRUD Operation: Update User."""

        with Session(ENGINE) as session:
            user = session.get(User, model_id)

            if user is None:
                raise UserError("User Not Found.")

            for key, value in data.model_dump().items():
                if value is None:
                    continue

                if key == "password":
                    valid_password = str(get_hash_value(value, str(user.salt_value)))
                    setattr(user, key, valid_password)
                else:
                    setattr(user, key, value)

            try:
                session.add(user)
                session.commit()
                session.refresh(user)
            except IntegrityError as exc:
                raise UserError("User not Updated.") from exc

            return user

    @validate_call
    def delete(self, model_id: UUID) -> str:
        """CRUD Operation: Delete User."""

        with Session(ENGINE) as session:
            user = session.get(User, model_id)

            if not user:
                raise UserError("User Not Found")

            try:
                session.delete(user)
                session.commit()
            except IntegrityError as exc:
                raise UserError("User not Deleted.") from exc

            return f"Deleted: {model_id}"

    @validate_call
    def get_user_id(self, data: CreateUserData) -> UUID:
        """Get User by Email."""

        with Session(ENGINE) as session:
            query = select(User).where(
                User.email == data.email,
            )
            user = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserError("User Not Found.")

            password = get_hash_value(data.password, str(user.salt_value))
            if str(user.password) != password:
                raise UserError("Invalid User Credentials.")

            return cast(UUID, user.id)