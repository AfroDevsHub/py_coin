"""Tests: Testing Configuration Module."""

from pytest import fixture
from sqlalchemy.orm import Session

from lib.exceptions import ApplicationError
from models import ENGINE
from tests.test_utils.blockchain import (
    create_blocks,
    create_contracts,
    create_transactions,
)
from tests.test_utils.users import (
    create_accounts,
    create_cards,
    create_logins,
    create_payment_profiles,
    create_settings,
    create_user_profiles,
    create_users,
)
from tests.test_utils.utils import (
    generate_socials,
    run_test_teardown,
    setup_test_commit,
)


@fixture
def get_socials() -> dict[str, str]:
    """Returns Test Social Media Links."""

    result = generate_socials()
    if not isinstance(result, dict):
        raise ApplicationError("Error Running Social Media Links.")
    return result


@fixture
def get_users():
    """Returns Test Users."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        yield users

        run_test_teardown([*users], session)


@fixture
def get_accounts():
    """Returns Test Accounts."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        accounts = create_accounts(list(map(lambda user: user.id, users)))
        setup_test_commit(accounts, session)

        yield accounts

        run_test_teardown([*accounts, *users], session)


@fixture
def get_settings():
    """Returns Test Setting Profiles."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        accounts = create_accounts(list(map(lambda user: user.id, users)))
        setup_test_commit(accounts, session)

        settings = create_settings(list(map(lambda account: account.id, accounts)))
        setup_test_commit(settings, session)

        yield settings

        run_test_teardown([*settings, *accounts, *users], session)


@fixture
def get_cards():
    """Returns Test Cards."""

    with Session(ENGINE) as session:
        cards = create_cards()
        setup_test_commit(cards, session)

        yield cards

        run_test_teardown(cards, session)


@fixture
def get_payments():
    """Returns Test Payments Profiles."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        accounts = create_accounts(list(map(lambda user: user.id, users)))
        setup_test_commit(accounts, session)

        cards = create_cards()
        setup_test_commit(cards, session)

        payments = create_payment_profiles(
            list(map(lambda account: account.id, accounts)),
            list(map(lambda card: card.id, cards)),
        )
        setup_test_commit(payments, session)

        yield payments

        run_test_teardown([*payments, *accounts, *cards, *users], session)


@fixture
def get_profiles():
    """Returns Test User Profiles."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        accounts = create_accounts(list(map(lambda user: user.id, users)))
        setup_test_commit(accounts, session)

        user_profiles = create_user_profiles(
            list(map(lambda account: account.id, accounts))
        )
        setup_test_commit(user_profiles, session)

        yield user_profiles

        run_test_teardown([*user_profiles, *accounts, *users], session)


@fixture
def get_logins():
    """Returns Test Logins History."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        logins = create_logins(list(map(lambda user: user.id, users)))
        setup_test_commit(logins, session)

        yield logins

        run_test_teardown([*logins, *users], session)


@fixture
def get_transactions():
    """Returns Test Transactions."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        accounts = create_accounts(list(map(lambda user: user.id, users)))
        setup_test_commit(accounts, session)

        cards = create_cards()
        setup_test_commit(cards, session)

        payments = create_payment_profiles(
            list(map(lambda account: account.id, accounts)),
            list(map(lambda card: card.id, cards)),
        )
        setup_test_commit(payments, session)

        transactions = create_transactions(
            list(map(lambda payment: payment.id, payments)),
            list(map(lambda payment: payment.id, list(reversed(payments)))),
            list(map(lambda card: card.card_id, cards)),
            list(map(lambda card: card.card_id, list(reversed(cards)))),
        )
        setup_test_commit(transactions, session)

        yield transactions

        run_test_teardown(
            [*transactions, *payments, *accounts, *cards, *users], session
        )


@fixture
def get_contracts():
    """Returns Test Contracts."""

    with Session(ENGINE) as session:
        users = create_users()
        setup_test_commit(users, session)

        accounts = create_accounts(list(map(lambda user: user.id, users)))
        setup_test_commit(accounts, session)

        cards = create_cards()
        setup_test_commit(cards, session)

        payments = create_payment_profiles(
            list(map(lambda account: account.id, accounts)),
            list(map(lambda card: card.id, cards)),
        )
        setup_test_commit(payments, session)

        contracts = create_contracts(
            list(map(lambda payment: payment.id, payments)),
            list(map(lambda payment: payment.id, list(reversed(payments)))),
            list(map(lambda card: card.card_id, cards)),
            list(map(lambda card: card.card_id, list(reversed(cards)))),
        )
        setup_test_commit(contracts, session)

        yield contracts

        run_test_teardown([*contracts, *payments, *accounts, *cards, *users], session)


@fixture
def get_blocks():
    """Returns Test Blocks."""

    with Session(ENGINE) as session:
        blocks = create_blocks()
        setup_test_commit(blocks, session)

        yield blocks

        run_test_teardown(blocks, session)
