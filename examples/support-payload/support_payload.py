"""Strict, side-effect-free validation of a support-ticket payload."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints


class SupportTicket(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True, frozen=True, str_strip_whitespace=True
    )

    title: Annotated[str, StringConstraints(min_length=1, max_length=120)]
    description: Annotated[str, StringConstraints(min_length=1, max_length=2000)]
    priority: Literal["low", "normal", "high"] = "normal"


def validate_support_payload(payload: object) -> SupportTicket:
    """Return a validated model or raise pydantic.ValidationError.

    No network, storage, coercion of numeric values to strings, or input mutation.
    This validates structure only: it is not authorization or HTML sanitization.
    """
    return SupportTicket.model_validate(payload)
