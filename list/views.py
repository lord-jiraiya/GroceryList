from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, ItemList
from datetime import date

@login_required(login_url='login')
def index(request):
    dueDate_Param = request.GET.get('dueDate')
    if dueDate_Param:
        groceryList = ItemList.objects.filter(dueDate__range=["0001-01-01",dueDate_Param])
    else:
        groceryList = ItemList.objects.filter(user = request.user)
	
    print(groceryList)

    return render(request, "list/index.html", {
        "gList" : groceryList
            })








@login_required(login_url='login')
def list_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            itemName = request.POST["item_name"]
            itemQuantity = request.POST["item_quant"]
            user = request.user
            itemStatus = request.POST["item_status"]
            date = request.POST["item_date"]
            try:
                newlist = ItemList.objects.create(itemName=itemName, itemQuantity=itemQuantity,
                                                     user=user, itemStatus=itemStatus,
                                                     dueDate=date)
                newlist.save()

                return HttpResponseRedirect(reverse("index"))

            except:
                return render(request, 'list/error.html', {
                    'message': "Sorry,\n Unexpected Error Occurred",
                })
        else:
            return render(request, "list/add.html", {
            })
    else:
        return HttpResponseRedirect(reverse("login"))






def modify_list(request,id):
    item = ItemList.objects.filter(id=id, user = request.user)
    if request.user.is_authenticated:
        if request.method == "DELETE":
            # print("Inside Yuo")
            item.delete()
            return JsonResponse(
                {
                     "success": 'true',
                    "redirect":'true',"redirect_url":"/"}
            )


        elif request.method == "POST":
            itemName = request.POST["item_name"]
            itemQuantity = request.POST["item_quant"]
            itemStatus = request.POST["item_status"]
            date = request.POST["item_date"]
            try:
                updateList = ItemList.objects.filter(user=request.user,id=id)[0]
                updateList.itemName = itemName
                updateList.itemQuantity = itemQuantity
                updateList.itemStatus = itemStatus
                updateList.dueDate = date
                updateList.save()

                print("done")

                return HttpResponseRedirect(reverse("index"))

            except:
                return render(request, 'list/error.html', {
                    'message': "Sorry,\n Unexpected Error Occurred",
                })
        else:
            return render(request, "list/update.html", {
                "item": item[0],
            })
    else:
        return HttpResponseRedirect(reverse("login"))













def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "list/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "list/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "list/register.html")



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
            return render(request, "list/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "list/login.html")






@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))