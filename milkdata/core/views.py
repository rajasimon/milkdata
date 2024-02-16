from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


from milkdata.core.models import Shed, ShedData, Pocket, Vendor, VendorData
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
        endpoint = reverse("shed_entry") + f"?shed={shed_param}"
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
            {"sheddata": sheddata, "shed": shed, "sheddatas": sheddatas},
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


def distribute(request):
    date = request.session["date"]
    sheds = Shed.objects.all()

    pocket, _ = Pocket.objects.get_or_create(date=date)
    vendors = Vendor.objects.all()

    total_milk = 0
    for shed in sheds:
        for shed_data in shed.sheddata_set.filter(date=date).all():
            total_milk += shed_data.value

    if request.method == "POST":
        half_litre = request.POST.get("half_litre")
        quarter_litre = request.POST.get("quarter_litre")

        if half_litre:
            pocket.half_litre = half_litre

        if quarter_litre:
            pocket.quarter_litre = quarter_litre

        pocket.save()

        return HttpResponseRedirect(reverse("distribute"))

    response = render(
        request,
        "distribute.html",
        {
            "sheds": sheds,
            "total_milk": round(total_milk, 3),
            "pocket": pocket,
            "vendors": vendors,
        },
    )

    if request.htmx:
        response.headers.set("HX-Redirect", reverse("index", kwargs={"date": date}))

    return response


def vendor_index(request):
    vendors = Vendor.objects.all()
    return render(request, "vendor_index.html", {"vendors": vendors})


def vendor_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")

        vendor, _ = Vendor.objects.get_or_create(name=name)
        vendor.category = category
        vendor.save()
        return HttpResponseRedirect(reverse("vendor_index"))

    return render(request, "vendor_create.html")


def vendor_edit(request, pk):
    vendor = Vendor.objects.filter(pk=pk).first()
    if request.method == "POST":
        name = request.POST.get("name")
        category = int(request.POST.get("category", 1))

        vendor.name = name
        vendor.category = category
        vendor.save()
        return HttpResponseRedirect(reverse("vendor_index"))

    return render(request, "vendor_edit.html", {"vendor": vendor})


def vendor_data(request, vendor_pk):
    date = request.session["date"]
    vendor = Vendor.objects.filter(pk=vendor_pk).first()
    if request.method == "POST":
        half_litre = int(request.POST.get("half_litre", 0))
        quarter_litre = int(request.POST.get("quarter_litre", 0))

        additional = request.POST.get("additional")
        if not additional:
            additional = 0
        note = request.POST.get("note")

        obj, _ = VendorData.objects.get_or_create(vendor=vendor, date=date)

        obj.half_litre = half_litre
        obj.quarter_litre = quarter_litre
        obj.additional = additional
        obj.note = note
        obj.save()

    return HttpResponseRedirect(reverse("distribute"))
