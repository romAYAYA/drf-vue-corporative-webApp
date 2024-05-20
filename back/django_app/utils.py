import re
from rest_framework.response import Response


def update_rating(instance, user, is_liked, rating_model):
    try:
        rating = rating_model.objects.get(
            author=user, **{instance.__class__.__name__.lower(): instance}
        )
        if rating.is_liked == is_liked:
            rating.delete()
        else:
            rating.is_liked = is_liked
            rating.save()
    except rating_model.DoesNotExist:
        rating_model.objects.create(
            author=user,
            **{instance.__class__.__name__.lower(): instance},
            is_liked=is_liked,
        )

    rating_sum = sum(
        1 if r.is_liked else -1
        for r in rating_model.objects.filter(
            **{instance.__class__.__name__.lower(): instance}
        )
    )
    return rating_sum


def rate_item(request, item_id, model, rating_model):
    try:
        item = model.objects.get(id=item_id)
    except model.DoesNotExist:
        return Response({"error": f"{model.__name__} not found"}, status=404)

    is_liked = request.data.get("is_liked")
    if is_liked not in [True, False]:
        return Response({"error": "Invalid rating value"}, status=400)

    rating_sum = update_rating(item, request.user, is_liked, rating_model)
    return Response({"rating": rating_sum}, status=200)


def get_item_rating(item_id, model, rating_model):
    try:
        item = model.objects.get(id=item_id)
    except model.DoesNotExist:
        return Response({"error": f"{model.__name__} not found"}, status=404)

    rating_sum = rating_model.objects.filter(item=item).aggregate(sum("is_liked"))[
        "is_liked__sum"
    ]
    rating_sum = rating_sum if rating_sum is not None else 0
    return Response({"rating": rating_sum}, status=200)


def password_check(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    return bool(re.match(pattern, password))


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
