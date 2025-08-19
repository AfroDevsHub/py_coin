"""Users: Serialiser for User Model."""

from typing import cast
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from pydantic import validate_call

from lib.interfaces.exceptions import UserError
from lib.interfaces.user.users import CreateUserData, UpdateUserData
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.user.users import User
from serialisers.serialiser import ISerialiser


class UserSerialiser(ISerialiser):
    """Serialiser for the User Model."""

    @validate_call
    def create(self, data: CreateUserData) -> User:
        """CRUD Operation: Create User."""

        with Session(ENGINE) as session:
            salt_value = uuid4()
            password = get_hash_value(data.password, str(salt_value))
            user = User(email=data.email, password=password, salt_value=salt_value)

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