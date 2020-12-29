import csv
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Type, Field, Schema, Schema_Field

def index(request):
    types = Type.objects.all()
    return render(request, "schemagen/index.html", {
        "type_list": types,
    })


@csrf_exempt
@login_required
def generation_data(request):
#TODO с фронта ИД схемы 

    table_name = 'table_name_TEMP' #TODO !! временно сюда внести имя, которое придумала пользователь
    row_count = 50 #TODO !! временно сюда внести колличество, которое указал пользователь
    file_url = 'media/'+ table_name  + '.csv'
    with open(file_url, 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['col1','col2','col3'])
        for i in range(row_count):
            thewriter.writerow(['one','two','three'])

    return JsonResponse({"message": "Post posted successfully.", "result": "Generation of data done" }, status=201)

@csrf_exempt
@login_required
def submit_schema(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    name = data["name"]

    schema = Schema.objects.create(name=name, user = request.user)
    schema.save()
    fields = Field.objects.all()
    for field in fields:
        list_schema_field = Schema_Field.objects.create(schema=schema, field=field)
        list_schema_field.save()
        #и пробижаться по всем текущим полям + ИД как раз созданной схемы'''
    return JsonResponse({"message": "Post posted successfully.", "data": schema.serialize() }, status=201)





@csrf_exempt
@login_required
def add_custom_field(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    name = data["name"]
    type_name = data["type"]
    order = data["order"]

    _type = Type.objects.get(name=type_name)

    field = Field.objects.create(name=name, _type=_type, order=order)
    field.save()
    return JsonResponse({"message": "Post posted successfully.", "data": field.serialize() }, status=201)





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