from flask import Blueprint, request
from app.middleware.auth_middleware import require_api_key
from app.services.report_service import low_stock, sales_summary
from app.utils.error_handler import error_response

report_bp = Blueprint("report", __name__)


# LOW STOCK REPORT
@report_bp.route("/api/v1/reports/low-stock")
@require_api_key("admin")
def low_stock_report():

    threshold = request.args.get("threshold", type=int)

    if threshold is None:
        return error_response("Threshold required", "REP001", 400)

    return low_stock(threshold)


# SALES SUMMARY REPORT
@report_bp.route("/api/v1/reports/sales-summary")
@require_api_key("admin")
def sales_report():
    return sales_summary()
