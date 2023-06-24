from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

#testing fetching messages
def test_fetch_messages():
    response = client.get("/api/messages")
    assert response.status_code == 200

#todo:
#test fetching a specific message
#test fetching a non existant specific message
#test deleting assigned message codes

#testing fetching codes
def test_fetch_codes():
    response = client.get("/api/codes")
    assert response.status_code == 200

#testing assigning codes to messages
def test_assign_codes():
    response = client.post(
        "api/assign_codes",
        json={
            "message_id": 1,
            "code_id": 1,
            "assigned_substring": "test",
        })
    assert response.status_code == 200
    assert response.json() == {
        "message_id": 1,
        "code_id": 1,
        "assigned_substring": "test",
    }

#testing assigning inexistant code
def test_assign_inexistant_code():
    response = client.post(
        "api/assign_codes",
        json={
            "message_id": "message_id",
            "assigned_codes": "inexistant_code"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Code not found"}

#testing fetching messages with their assigned code(s)
def test_fetch_assigned_codes():
    response = client.get("/api/assigned/message_id")
    assert response.status_code == 200
    assert response.json() == {
        "message_id": "message_id",
        "assigned_codes": "assigned_codes"
    }