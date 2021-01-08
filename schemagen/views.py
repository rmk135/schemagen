import csv
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Field, Schema, Schema_Field
from . import fields_types


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user
    schemas = Schema.objects.filter(user=user)
    return render(request, "schemagen/index.html", {
            "type_list": fields_types.type_list,
            "schemas": schemas
        })


@csrf_exempt
@login_required
def generation_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    table_name = data["table_name"]
    row_count = int(data["count_rows"])
    file_url = 'media/' + table_name + '.csv'
    schema_id = data["schema_id"]

    schema = Schema.objects.get(id=schema_id)

    column_list_name = [
            schema_field.field.name
            for schema_field in Schema_Field.objects.filter(schema=schema)
        ]
    rows = schema.get_rows(row_count)

    with open(file_url, 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(column_list_name)
        for i in range(len(rows)):
            thewriter.writerow(rows[i])

    return JsonResponse({"message": "Post posted successfully.",
                         "result": "Generation of data done"}, status=201)


@csrf_exempt
@login_required
def submit_schema(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    name = data["name"]

    schema = Schema.objects.create(name=name, user=request.user)
    schema.save()
    fields = Field.objects.all()
    for field in fields:
        schema_fields = Schema_Field.objects.create(schema=schema, field=field)
        schema_fields.save()
    return JsonResponse({"message": "Post posted successfully.",
                         "data": schema.serialize()}, status=201)


@csrf_exempt
@login_required
def add_custom_field(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    name = data["name"]
    kind = data["kind"]
    order = data["order"]

    field = Field.objects.create(name=name, kind=kind, order=order)
    field.save()
    return JsonResponse({"message": "Post posted successfully.",
                         "data": field.serialize()}, status=201)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "schemagen/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "schemagen/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "schemagen/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "schemagen/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "schemagen/register.html")
