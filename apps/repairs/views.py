from django.views.generic import View
from django.http import JsonResponse

from .services import get_latest_repair_by_phone


class TrackApiView(View):
    def get(self, request):
        phone = request.GET.get("phone", "").strip()
        if not phone:
            return JsonResponse(
                {"found": False, "message": "شماره موبایل را وارد کنید."},
                status=400,
            )

        order = get_latest_repair_by_phone(phone)
        if not order:
            return JsonResponse(
                {"found": False, "message": "سفارشی با این شماره یافت نشد."}
            )

        # 4-step timeline:
        #   status 0 (received)   -> step 0 active
        #   status 1 (inspecting) -> step 1 active
        #   status 2 (repairing)  -> step 2 active
        #   status 3 (ready)      -> step 3 active
        #   status 4 (delivered)  -> all steps done
        current_step = min(order.status_index, 4)

        return JsonResponse(
            {
                "found": True,
                "order": {
                    "id": str(order.id)[:8],
                    "status": order.get_status_display(),
                    "status_index": order.status_index,
                    "current_step": current_step,
                    "progress": order.progress_percent,
                    "device": order.device_model or "—",
                    "customer": order.customer_name,
                    "estimated_delivery": (
                        order.estimated_delivery.strftime("%Y/%m/%d %H:%M")
                        if order.estimated_delivery
                        else None
                    ),
                },
            }
        )