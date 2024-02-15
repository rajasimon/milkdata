from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


from milkdata.core.models import Shed, ShedData, Pocket, Shop, ShopData
from milkdata.core.helper import get_today_date


def index(request):
    return render(request, "index.html")


def shed_entry(request):
    date = request.session["date"]

    # Sending all the available sheds, shed, sheddata
    sheds = Shed.objects.all()
    shed_param = request.GET.get("shed", "")
    if shed_param:
        shed = Shed.objects.filter(name=shed_param).first()
    else:
        shed = Shed.objects.first()

    sheddatas = shed.sheddata_set.filter(date=date).all()
    response = render(
        request,
        "shed_entry.html",
        {"shed": shed, "sheds": sheds, "sheddatas": sheddatas},
    )

    if request.htmx:
        endpoint = reverse("index") + f"?shed={shed_param}"
        response["HX-Redirect"] = endpoint

    return response


def date_index(request):
    if request.method == "POST":
        date = request.POST.get("date")
        if date:
            request.session["date"] = date

        return HttpResponseRedirect(reverse("index"))

    return render(request, "date_index.html")


def shed_index(request):
    sheds = Shed.objects.all()
    return render(request, "shed_index.html", {"sheds": sheds})


def shed_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        shed, _ = Shed.objects.get_or_create(name=name)

        return HttpResponseRedirect(reverse("shed_index"))
    return render(request, "shed_create.html")


def shed_data_create(request, shed_name):
    date = request.session["date"]
    shed = Shed.objects.filter(name=shed_name).first()

    if request.method == "POST":
        value = request.POST["value"]
        sheddata = ShedData.objects.create(shed=shed, date=date, value=value)

        sheddatas = shed.sheddata_set.filter(date=date).all()
        return render(
            request,
            "shed_data.html",
            {"shed_data": sheddata, "shed": shed, "sheddatas": sheddatas},
        )
    return render(request, "shed_data.html")


def shed_data_edit(request, shed_data_pk):
    shed_data = ShedData.objects.get(pk=shed_data_pk)

    if request.method == "POST":
        value = request.POST["value"]
        shed_data.value = value
        shed_data.save()

        endpoint = reverse("index") + f"?shed={shed_data.shed.name}"
        return HttpResponseRedirect(endpoint)

    return render(request, "shed_data_edit.html", {"shed_data": shed_data})


def prepare(request):
    date = request.session["date"]
    sheds = Shed.objects.all()

    pocket, _ = Pocket.objects.get_or_create(date=date)
    shops = Shop.objects.all()

    total_milk = 0
    for shed in sheds:
        for shed_data in shed.sheddata_set.filter(date=date).all():
            total_milk += shed_data.value

    if request.method == "POST":
        half_litre = request.POST.get("half_litre")
        quarter_litre = request.POST.get("quarter_litre")
        shop_pk = request.POST.get("shop_pk", "")

        if half_litre:
            pocket.half_litre = half_litre

        if quarter_litre:
            pocket.quarter_litre = quarter_litre

        pocket.save()

        return HttpResponseRedirect(reverse("prepare"))

    response = render(
        request,
        "prepare.html",
        {"sheds": sheds, "total_milk": total_milk, "pocket": pocket, "shops": shops},
    )

    if request.htmx:
        response.headers.set("HX-Redirect", reverse("index", kwargs={"date": date}))

    return response


def shop_index(request):
    shops = Shop.objects.all()
    return render(request, "shop_index.html", {"shops": shops})


def shop_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")

        shop, _ = Shop.objects.get_or_create(name=name)
        shop.category = category
        shop.save()
        return HttpResponseRedirect(reverse("shop_index"))

    return render(request, "shop_create.html")


def shop_edit(request, pk):
    shop = Shop.objects.filter(pk=pk).first()
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")

        shop.category = category
        shop.save()
        return HttpResponseRedirect(reverse("shop_index"))

    return render(request, "shop_edit.html", {"shop": shop})


def shop_data(request, shop_pk):
    date = request.session["date"]
    shop = Shop.objects.filter(pk=shop_pk).first()
    if request.method == "POST":
        half_litre = int(request.POST.get("half_litre", 0))
        quarter_litre = int(request.POST.get("quarter_litre", 0))
        additional = int(request.POST.get("additional", 0))
        tray = int(request.POST.get("tray", 0))

        obj, _ = ShopData.objects.get_or_create(shop=shop, date=date)

        obj.half_litre = half_litre
        obj.quarter_litre = quarter_litre
        obj.additional = additional
        obj.tray = tray

        if shop.category == 2:
            if not half_litre:
                if tray and additional:
                    per_tray = 24
                    total_half_litre = (per_tray * tray) + additional
                    obj.half_litre = total_half_litre

        obj.save()

    return HttpResponseRedirect(reverse("prepare"))
