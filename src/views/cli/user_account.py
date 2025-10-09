# Example function to display account info in sections using inquirer

from inquirer import Confirm, prompt

from models.user.accounts import Account


def display_account_sections(account: Account) -> None:
    # Section 1: Account Level Info
    print("\n=== [Account Information] ===")
    print(f"Account ID: {account.id}")
    print(f"Created Date: {account.created_date}")
    print(f"Status: {account.status}")
    print(f"User: {account.user_id}")

    prompt([Confirm("next", message="Continue to User Profile?", default=True)])

    # Section 2: User Profile
    user_profile = account.user_profiles

    print("\n=== [User Profile] ===")
    if user_profile:
        print(f"First Name      : {user_profile.first_name or 'N/A'}")
        print(f"Last Name       : {user_profile.last_name or 'N/A'}")
        print(f"Username        : {user_profile.username or 'N/A'}")
        print(f"Date of Birth   : {user_profile.date_of_birth or 'N/A'}")
        print(
            f"Gender          : {getattr(user_profile.gender, 'name', user_profile.gender) if user_profile.gender else 'N/A'}"
        )
        print(f"Mobile Number   : {user_profile.mobile_number or 'N/A'}")
        print(
            f"Country         : {getattr(user_profile.country, 'name', user_profile.country) if user_profile.country else 'N/A'}"
        )
        print(
            f"Language        : {getattr(user_profile.language, 'name', user_profile.language) if user_profile.language else 'N/A'}"
        )
        print(f"Biography       : {user_profile.biography or 'N/A'}")
        print(
            f"Occupation      : {getattr(user_profile.occupation, 'name', user_profile.occupation) if user_profile.occupation else 'N/A'}"
        )
        print(
            f"Interests       : {', '.join([i.name if hasattr(i, 'name') else str(i) for i in (user_profile.interests or [])]) or 'N/A'}"
        )
        print(f"Social Links    : {user_profile.social_media_links or '{}'}")
        print(
            f"Status          : {getattr(user_profile.status, 'name', user_profile.status) if user_profile.status else 'N/A'}"
        )
        print(f"Created Date    : {user_profile.created_date or 'N/A'}")
        print(f"Updated Date    : {user_profile.updated_date or 'N/A'}")
        prompt([Confirm("next", message="Continue to Settings?", default=True)])
    else:
        print("No user profile found.")

    # Section 3: Settings
    settings = account.settings_profile
    print("\n=== [Settings] ===")

    if settings:
        print(f"Settings ID                : {settings.id}")
        print(f"Settings Profile ID        : {settings.settings_id}")
        print(f"Account ID                 : {settings.account_id}")
        print(
            f"Email Status               : {getattr(settings.email_status, 'name', settings.email_status) if settings.email_status else 'N/A'}"
        )
        print(
            f"Communication Status       : {getattr(settings.communication_status, 'name', settings.communication_status) if settings.communication_status else 'N/A'}"
        )
        print(f"MFA Enabled                : {settings.mfa_enabled}")
        print(f"MFA Last Used Date         : {settings.mfa_last_used_date or 'N/A'}")
        print(
            f"Profile Visibility         : {getattr(settings.profile_visibility_preference, 'name', settings.profile_visibility_preference) if settings.profile_visibility_preference else 'N/A'}"
        )
        print(
            f"Data Sharing Preferences   : {', '.join([p.name if hasattr(p, 'name') else str(p) for p in (settings.data_sharing_preferences or [])]) or 'N/A'}"
        )
        print(
            f"Communication Preference   : {getattr(settings.communication_preference, 'name', settings.communication_preference) if settings.communication_preference else 'N/A'}"
        )
        print(f"Location Tracking Enabled  : {settings.location_tracking_enabled}")
        print(f"Cookies Enabled            : {settings.cookies_enabled}")
        print(
            f"Theme Preference           : {getattr(settings.theme_preference, 'name', settings.theme_preference) if settings.theme_preference else 'N/A'}"
        )
        print(f"Created Date               : {settings.created_date or 'N/A'}")
        print(f"Updated Date               : {settings.updated_date or 'N/A'}")
    else:
        print("No settings profile found.")

    prompt([Confirm("next", message="Continue to Payments?", default=True)])

    # Section 4: Payments
    print("\n=== [Payments] ===")

    payment = account.payment_profiles
    if payment:
        print(f"Payment Profile ID : {payment.id}")
        print(f"Payment ID         : {payment.payment_id}")
        print(f"Account ID         : {payment.account_id}")
        print(f"Card ID            : {payment.card_id}")
        print(f"Name               : {payment.name}")
        print(f"Description        : {payment.description}")
        print(
            f"Status             : {getattr(payment.status, 'name', payment.status) if payment.status else 'N/A'}"
        )
        print(f"Balance            : {payment.balance}")
        print(f"Created Date       : {payment.created_date or 'N/A'}")
        print(f"Updated Date       : {payment.updated_date or 'N/A'}")
        print("-" * 40)
    else:
        print("No payment profile found.")

    print("\n=== [End of Account Details] ===")
    prompt([Confirm("next", message="Return to main menu?", default=True)])
