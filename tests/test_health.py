
def test_health_get(client):
    response = client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_post(client):
    health_data = {"some_key": "some_value"}  
    response = client.post("/api/v1/health", json=health_data)
    assert response.status_code == 200
    assert response.json() == health_data

