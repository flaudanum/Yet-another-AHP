import pytest
from fastapi.testclient import TestClient

from web_api.models.layout import Layout
from web_api.server import app

client = TestClient(app)


def test_layout():
    req_body = {
        "root": "Goal",
        "dependencies": [
            ["Goal", "Criterion A"],
            ["Goal", "Criterion B"],
            ["Criterion A", "Criterion C"],
            ["Criterion A", "Criterion D"],
            ["Criterion B", "Criterion E"],
            ["Criterion B", "Criterion F"],
        ]
    }

    response = client.post(
        "/hierarchy/layout/",
        json=req_body,
    )

    # Response must have success status
    assert response.status_code == 200

    # Response body must be of type Layout (else a ValidationError is raised)
    Layout.parse_obj(response.json())
