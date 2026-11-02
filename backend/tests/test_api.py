from models import Item


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


class TestItems:
    def test_get_items_empty(self, client):
        response = client.get("/api/items")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_items(self, client, db_session):
        db_session.add(Item(name="First"))
        db_session.commit()

        response = client.get("/api/items")
        assert response.status_code == 200
        assert [i["name"] for i in response.json()] == ["First"]

    def test_get_item(self, client, db_session):
        item = Item(name="First", description="Hello")
        db_session.add(item)
        db_session.commit()

        response = client.get(f"/api/items/{item.id}")
        assert response.status_code == 200
        assert response.json()["description"] == "Hello"

    def test_get_item_not_found(self, client):
        assert client.get("/api/items/999").status_code == 404

    def test_create_item(self, client):
        response = client.post("/api/items", json={"name": "New"})
        assert response.status_code == 201
        assert response.json()["name"] == "New"
        assert client.get("/api/items").json()[0]["name"] == "New"

    def test_create_item_validation(self, client):
        assert client.post("/api/items", json={"name": ""}).status_code == 422

    def test_update_item(self, client, db_session):
        item = Item(name="Old", description="Kept")
        db_session.add(item)
        db_session.commit()

        response = client.patch(f"/api/items/{item.id}", json={"name": "New"})
        assert response.status_code == 200
        assert response.json()["name"] == "New"
        assert response.json()["description"] == "Kept"

    def test_update_item_clears_description(self, client, db_session):
        item = Item(name="Item", description="Gone")
        db_session.add(item)
        db_session.commit()

        response = client.patch(
            f"/api/items/{item.id}", json={"description": None}
        )
        assert response.json()["description"] is None

    def test_update_item_validation(self, client, db_session):
        item = Item(name="Item")
        db_session.add(item)
        db_session.commit()

        url = f"/api/items/{item.id}"
        assert client.patch(url, json={"name": ""}).status_code == 422
        assert client.patch(url, json={"name": None}).status_code == 422

    def test_update_item_not_found(self, client):
        response = client.patch("/api/items/999", json={"name": "X"})
        assert response.status_code == 404

    def test_delete_item(self, client, db_session):
        item = Item(name="Doomed")
        db_session.add(item)
        db_session.commit()

        assert client.delete(f"/api/items/{item.id}").status_code == 204
        assert client.get("/api/items").json() == []

    def test_delete_item_not_found(self, client):
        assert client.delete("/api/items/999").status_code == 404


def test_allowed_origins_are_comma_separated(monkeypatch):
    from settings import Settings

    monkeypatch.setenv("ALLOWED_ORIGINS", "http://a.com, http://b.com")
    assert Settings().allowed_origins == ["http://a.com", "http://b.com"]
