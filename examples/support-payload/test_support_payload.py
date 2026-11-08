import copy

import pytest
from pydantic import ValidationError

from support_payload import validate_support_payload


def test_valid_payload_is_normalized_without_mutating_input():
    payload = {"title": "  Bouton inactif  ", "description": "  Aucun effet au clic.  "}
    before = copy.deepcopy(payload)

    ticket = validate_support_payload(payload)

    assert ticket.model_dump() == {
        "title": "Bouton inactif",
        "description": "Aucun effet au clic.",
        "priority": "normal",
    }
    assert payload == before
    assert validate_support_payload(ticket.model_dump()) == ticket
    assert validate_support_payload({
        "title": "x" * 120, "description": "x" * 2000, "priority": "high"
    }).priority == "high"
    with pytest.raises(ValidationError):
        ticket.priority = "low"


def test_invalid_payloads_are_rejected_without_mutation():
    valid = {"title": "Anomalie", "description": "Résultat inattendu"}
    invalid_payloads = [
        None, [], "texte", {},
        {**valid, "title": "   "},
        {**valid, "description": "\n\t"},
        {**valid, "title": "x" * 121},
        {**valid, "description": "x" * 2001},
        {**valid, "title": 42},
        {**valid, "description": False},
        {**valid, "priority": "urgent"},
        {**valid, "priority": None},
        {**valid, "admin": True},
    ]
    for payload in invalid_payloads:
        before = copy.deepcopy(payload)
        with pytest.raises(ValidationError):
            validate_support_payload(payload)
        assert payload == before
