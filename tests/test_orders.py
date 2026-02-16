def create_product(client, admin_key):
    client.post(
        "/api/v1/products",
        json={
            "sku": "P1",
            "name": "Phone",
            "price": 100,
            "stock_quantity": 10,
            "category": "electronics"
        },
        headers={"X-API-Key": admin_key}
    )


def create_order(client, admin_key):
    create_product(client, admin_key)

    res = client.post(
        "/api/v1/orders",
        json={
            "customer_name": "John",
            "customer_email": "john@test.com",
            "items": [{"product_id": 1, "quantity": 2}]
        },
        headers={"X-API-Key": admin_key}
    )

    return res.get_json()["order_id"]


def test_create_order(client, admin_key):
    order_id = create_order(client, admin_key)
    assert order_id is not None


def test_insufficient_stock(client, admin_key):
    create_product(client, admin_key)

    res = client.post(
        "/api/v1/orders",
        json={
            "customer_name": "John",
            "customer_email": "john@test.com",
            "items": [{"product_id": 1, "quantity": 100}]
        },
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 400


def test_cancel_order(client, admin_key):
    order_id = create_order(client, admin_key)

    res = client.post(
        f"/api/v1/orders/{order_id}/cancel",
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_order_status_update(client, admin_key):
    order_id = create_order(client, admin_key)

    res = client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "confirmed"},
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_invalid_status_update(client, admin_key):
    order_id = create_order(client, admin_key)

    res = client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "invalid"},
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 400
