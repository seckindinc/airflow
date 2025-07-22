from airflow.sdk import asset, Context, Asset
from typing import Dict, Any, Optional
from pendulum import datetime


@asset(
    schedule="@daily",
    description="User data source - generates user information",
    tags=["source", "user"],
)
def user_data() -> Dict[str, Any]:
    """Generate user data as the source asset."""
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "created_at": datetime.now().isoformat(),
    }


@asset(
    schedule=[user_data],
    description="Extracts user email from user data",
    tags=["transform", "email"],
)
def user_email(context: Context) -> str:
    """Extract email from user data asset."""
    # Get the user data from the upstream asset
    user_info = context["inlet_events"][user_data][-1].payload
    return user_info["email"]


@asset(
    schedule=[user_email],
    description="Parses email domain from user email",
    tags=["transform", "domain"],
)
def email_domain(context: Context) -> Optional[str]:
    """Parse domain from user email asset."""
    # Get the email from the upstream asset
    email = context["inlet_events"][user_email][-1].payload

    # Extract domain with proper error handling
    if not email or "@" not in email:
        return None

    parts = email.split("@")
    return parts[1] if len(parts) == 2 and parts[1] else None


@asset(
    schedule=[user_data, email_domain],
    description="Creates user profile combining user data and email domain",
    tags=["sink", "profile"],
)
def user_profile(context: Context) -> Dict[str, Any]:
    """Create complete user profile from multiple upstream assets."""
    # Get data from multiple upstream assets
    user_info = context["inlet_events"][user_data][-1].payload
    domain = context["inlet_events"][email_domain][-1].payload

    return {
        "user_id": user_info["id"],
        "name": user_info["name"],
        "email": user_info["email"],
        "domain": domain,
        "profile_created": datetime.now().isoformat(),
    }
