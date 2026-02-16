def create_sample_product(client, admin_key):
    return client.post(
        "/api/v1/products",
        json={
            "sku": "P100",
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 1000,
            "stock_quantity": 10,
            "category": "electronics"
        },
        headers={"X-API-Key": admin_key}
    )


def test_create_product(client, admin_key):
    res = create_sample_product(client, admin_key)
    assert res.status_code == 201


def test_update_product(client, admin_key):
    create_sample_product(client, admin_key)

    res = client.put(
        "/api/v1/products/1",
        json={"price": 900},
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_delete_product(client, admin_key):
    create_sample_product(client, admin_key)

    res = client.delete(
        "/api/v1/products/1",
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_stock_update(client, admin_key):
    create_sample_product(client, admin_key)

    res = client.patch(
        "/api/v1/products/1/stock",
        json={"adjust": 5},
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_product_search(client, admin_key):
    create_sample_product(client, admin_key)

    res = client.get(
        "/api/v1/products?search=Laptop",
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_invalid_product_input(client, admin_key):
    res = client.post(
        "/api/v1/products",
        json={},
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 400
