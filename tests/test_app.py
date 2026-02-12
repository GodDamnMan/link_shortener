from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_shorten_url():
    response = client.post("/shorten", json={"original_url": "https://example.com"})
    assert response.status_code == 201
    data = response.json()
    assert "shorten_url" in data


def test_custom_code():
    response = client.post(
        "/shorten",
        json={"original_url": "https://test.com", "custom_code": "myawesomecode"}
    )
    assert response.status_code == 201
    assert response.json()["shorten_url"] == "http://testserver/myawesomecode"


def test_redirect():
    shorten = client.post("/shorten", json={"original_url": "https://google.com"})
    shorten_url = shorten.json()["shorten_url"]

    redirect_resp = client.get(f"{shorten_url}", follow_redirects=False)
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers["location"] == "https://google.com/"


def test_not_found():
    response = client.get("/nonexistent12345")
    assert response.status_code == 404