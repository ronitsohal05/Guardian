from flask import Blueprint, request, jsonify

from core.email_service import send_notification_email
from core.auth import require_auth

email_bp = Blueprint("email", __name__, url_prefix="/email")


@email_bp.post("/send")
@require_auth
def send_email():
    """Send a test notification email. Protected endpoint for testing.

    JSON body:
      recipient_email: str (required)
      store_name: str (required)
      item: str (required)
      distance_km: number (optional)
      store_location: object (optional)
    """
    body = request.get_json(force=True) or {}
    recipient = (body.get("recipient_email") or "").strip()
    store_name = (body.get("store_name") or "").strip()
    item = (body.get("item") or "").strip()
    distance = body.get("distance_km", 0)
    store_location = body.get("store_location")

    if not recipient or "@" not in recipient:
        return jsonify({"error": "Valid recipient_email required"}), 400
    if not store_name:
        return jsonify({"error": "store_name required"}), 400
    if not item:
        return jsonify({"error": "item required"}), 400

    try:
        distance = float(distance or 0)
    except Exception:
        return jsonify({"error": "distance_km must be a number"}), 400

    ok = send_notification_email(
        recipient_email=recipient,
        store_name=store_name,
        item=item,
        distance_km=distance,
        store_location=store_location,
    )

    if ok:
        return jsonify({"ok": True, "sent_to": recipient})
    else:
        return jsonify({"ok": False, "error": "failed to send email (check SMTP settings)"}), 500
