def test_low_stock_report(client, admin_key):

    res = client.get(
        "/api/v1/reports/low-stock?threshold=50",
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200


def test_low_stock_missing_threshold(client, admin_key):

    res = client.get(
        "/api/v1/reports/low-stock",
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 400


def test_sales_summary(client, admin_key):

    res = client.get(
        "/api/v1/reports/sales-summary",
        headers={"X-API-Key": admin_key}
    )

    assert res.status_code == 200
