def test_missing_api_key(client):
    res = client.get("/api/v1/products")
    assert res.status_code == 401


def test_invalid_api_key(client):
    res = client.get(
        "/api/v1/products",
        headers={"X-API-Key": "wrong"}
    )
    assert res.status_code == 403


def test_role_denied(client, user_key):
    res = client.post(
        "/api/v1/products",
        json={"sku":"T1","name":"Item","price":10,"stock_quantity":5,"category":"test"},
        headers={"X-API-Key": user_key}
    )
    assert res.status_code == 403


def test_valid_admin_key(client, admin_key):
    res = client.get(
        "/api/v1/products",
        headers={"X-API-Key": admin_key}
    )
    assert res.status_code == 200
