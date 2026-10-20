from .models import RepairOrder


def get_latest_repair_by_phone(phone: str):
    if not phone:
        return None
    digits = "".join(filter(str.isdigit, phone))
    if len(digits) < 10:
        return None
    return (
        RepairOrder.objects.filter(phone__endswith=digits)
        .only("id", "status", "device_model", "estimated_delivery", "customer_name")
        .first()
    )