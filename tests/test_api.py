from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from notes.app import create_app

MISSING_ID = "00000000-0000-0000-0000-000000000001"


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "notes-test.sqlite"


@pytest.fixture
def client(db_path: Path) -> TestClient:
    return TestClient(create_app(db_path))


def _create(client: TestClient, *, title: str = "Shopping List", content: str = "Milk") -> dict:
    response = client.post("/notes", json={"title": title, "content": content})
    assert response.status_code == 201
    return response.json()


def test_create_note_returns_201_and_persisted_fields(client: TestClient) -> None:
    body = _create(client)

    assert body["title"] == "Shopping List"
    assert body["content"] == "Milk"
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"] == body["created_at"]


def test_get_note_returns_200_and_stored_data(client: TestClient) -> None:
    created = _create(client)

    response = client.get(f"/notes/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_note_returns_404(client: TestClient) -> None:
    response = client.get(f"/notes/{MISSING_ID}")

    assert response.status_code == 404
    assert response.json() == {"error": "Note not found"}


def test_list_notes_includes_created_notes(client: TestClient) -> None:
    first = _create(client, title="a", content="one")
    second = _create(client, title="b", content="two")

    response = client.get("/notes")

    assert response.status_code == 200
    ids = {note["id"] for note in response.json()}
    assert first["id"] in ids
    assert second["id"] in ids


def test_update_note_returns_200_and_refreshes_updated_at(client: TestClient) -> None:
    created = _create(client)

    response = client.put(
        f"/notes/{created['id']}",
        json={"title": "Updated title", "content": "Updated content"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["title"] == "Updated title"
    assert body["content"] == "Updated content"
    assert body["created_at"] == created["created_at"]
    assert body["updated_at"] != created["updated_at"]


def test_update_missing_note_returns_404(client: TestClient) -> None:
    response = client.put(
        f"/notes/{MISSING_ID}",
        json={"title": "t", "content": "c"},
    )

    assert response.status_code == 404
    assert response.json() == {"error": "Note not found"}


def test_delete_note_returns_204_then_get_is_404(client: TestClient) -> None:
    created = _create(client)

    deleted = client.delete(f"/notes/{created['id']}")
    fetched = client.get(f"/notes/{created['id']}")

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert fetched.status_code == 404


def test_delete_missing_note_returns_404(client: TestClient) -> None:
    response = client.delete(f"/notes/{MISSING_ID}")

    assert response.status_code == 404
    assert response.json() == {"error": "Note not found"}


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"content": "c"}, "title"),
        ({"title": "", "content": "c"}, "title"),
        ({"title": "   ", "content": "c"}, "title"),
        ({"title": "x" * 201, "content": "c"}, "title"),
        ({"title": "t"}, "content"),
        ({"title": "t", "content": ""}, "content"),
        ({"title": "t", "content": "   "}, "content"),
        ({"title": "t", "content": "x" * 10_001}, "content"),
    ],
)
def test_invalid_fields_return_422_with_details(
    client: TestClient, payload: dict[str, str], field: str
) -> None:
    response = client.post("/notes", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "Validation failed"
    assert field in body["details"]


def test_validation_failure_does_not_create_a_note(client: TestClient) -> None:
    client.post("/notes", json={"title": "", "content": "c"})

    assert client.get("/notes").json() == []


def test_validation_failure_does_not_modify_an_existing_note(client: TestClient) -> None:
    created = _create(client)

    response = client.put(
        f"/notes/{created['id']}",
        json={"title": "", "content": "changed"},
    )
    fetched = client.get(f"/notes/{created['id']}")

    assert response.status_code == 422
    assert fetched.json() == created


def test_malformed_json_returns_422(client: TestClient) -> None:
    response = client.post(
        "/notes",
        content=b"{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["error"] == "Validation failed"


def test_notes_survive_a_new_app_on_the_same_sqlite_file(db_path: Path) -> None:
    first = TestClient(create_app(db_path))
    created = _create(first)

    second = TestClient(create_app(db_path))
    fetched = second.get(f"/notes/{created['id']}")

    assert fetched.status_code == 200
    assert fetched.json()["title"] == created["title"]
    assert fetched.json()["content"] == created["content"]


def test_unknown_note_id_is_not_confused_with_a_random_uuid(client: TestClient) -> None:
    response = client.get(f"/notes/{uuid4()}")

    assert response.status_code == 404
