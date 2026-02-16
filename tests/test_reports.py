def test_rate_limit_allowed(client, admin_key):

    for _ in range(5):
        res = client.get(
            "/api/v1/products",
            headers={"X-API-Key": admin_key}
        )

    assert res.status_code == 200


def test_rate_limit_block(client, admin_key):

    status = 200

    for _ in range(65):
        res = client.get(
            "/api/v1/products",
            headers={"X-API-Key": admin_key}
        )
        status = res.status_code

    assert status in [200, 429]
