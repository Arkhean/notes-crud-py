from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

# CREATE ===============================================================================================================


def test_create_return_201():
    """
    Check that we can create a note.
    """
    response = client.post("/notes", json={"text": "hello"})
    assert response.status_code == 201
    response = response.json()
    assert response["text"] == "hello"


# GET BY ID ============================================================================================================


def test_get_by_id_return_200():
    assert False


def test_get_by_id_return_404():
    assert False


# SEARCH ===============================================================================================================


def test_search_return_200():
    assert False


# UPDATE ===============================================================================================================


def test_update_return_200():
    assert False


def test_update_return_404():
    assert False


# DELETE ===============================================================================================================


def test_delete_return_204():
    assert False


def test_delete_return_404():
    assert False
