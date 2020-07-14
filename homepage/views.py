from homepage.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json


def make_a_pagination(request, data):
    """ Paginate the database result """
    paginator = Paginator(data, 9)
    page = request.GET.get("page")
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return product


def index(request):
    """ simple views to load the homepage"""

    context = {"connected": request.user.is_authenticated}

    return render(request, "homepage/index.html", context)


def create(request):
    """ with post element send via the form, create
    a new user (if he doesn't exist in database) et log him"""

    name = request.POST["name"]
    mail = request.POST["mail"]
    password = request.POST["password"]

    u = User.objects.filter(email=mail)
    if not u.exists():
        User.objects.create_user(name, mail, password)

    user = authenticate(username=name, password=password)
    login(request, user)

    context = {"connected": request.user.is_authenticated}

    return render(request, "homepage/index.html", context)


def login_user(request):
    """ Log the user with post elments send via the form """

    name = request.POST["name"]
    password = request.POST["password"]
    user = authenticate(username=name, password=password)
    if user is not None:
        login(request, user)

    context = {"connected": request.user.is_authenticated}

    return render(request, "homepage/index.html", context)


def logout_user(request):
    """ Disconnect user"""
    logout(request)

    context = {"connected": request.user.is_authenticated}

    return render(request, "homepage/index.html", context)


def account(request):
    """load the profil page of the user"""

    name = request.user.get_username()
    mail = request.user.email
    title = "Bonjour %s !" % name

    context = {
        "title": title,
        "email": mail,
        "connected": request.user.is_authenticated,
    }

    return render(request, "homepage/login.html", context)


def substituts(request, id):
    """ Select all product with an healthier nutriscore and
    verify if product is in favoris user"""

    selection = Product.objects.get(id=id)
    product_list = Product.objects.filter(
        id_category=selection.id_category, nutriscore__lt=selection.nutriscore
    ).order_by("nutriscore")

    product = make_a_pagination(request, product_list)

    favoris = []
    if request.user.is_authenticated:
        for elt in Favoris.objects.filter(user=request.user):
            favoris.append(elt.product_id)

    if len(product) > 0:
        subtitle = "Vous pouvez remplacer cet aliment par :"
    else:
        subtitle = "Désolé, nous n'avons trouvé aucun substitut plus sain pour le produit séléctionné"

    context = {
        "request": "substitut",
        "title": selection.name,
        "subtitle": subtitle,
        "product": product,
        "connected": request.user.is_authenticated,
        "url": selection.image,
        "favoris": favoris,
        "paginate": True,
    }

    return render(request, "homepage/list.html", context)


def search(request):
    """ search in database all product of the same category
    that match with query user"""

    query_data = request.GET.get("query")

    product_list = Product.objects.filter(name__icontains=query_data)
    if not product_list.exists():
        product_list = Product.objects.filter(brand__icontains=query_data)

    product = make_a_pagination(request, product_list)

    if len(product_list) == 0:
        subtitles = "Désolé aucun produit ne correspond à votre recherche"
    else:
        subtitles = "choisissez un produit"

    title = "Résultats pour la requête '%s'" % query_data
    context = {
        "request": "results",
        "title": title,
        "subtitle": subtitles,
        "product": product,
        "connected": request.user.is_authenticated,
        "q": query_data,
        "paginate": True,
    }

    return render(request, "homepage/list.html", context)


def detail(request, id):
    """ load detail page of the selected product"""

    detail = Product.objects.get(id=id)

    context = {
        "product": detail,
        "connected": request.user.is_authenticated,
        "url": detail.image,
    }

    return render(request, "homepage/detail.html", context)


def favoris(request):
    """ load all saved product of the user"""

    product_list = Favoris.objects.filter(user=request.user)
    product = make_a_pagination(request, product_list)

    context = {
        "request": "favoris",
        "title": "mes aliments",
        "subtitle": "Retrouvez ici tous vos aliments préférés !",
        "product": product,
        "connected": request.user.is_authenticated,
        "paginate": True,
    }

    return render(request, "homepage/list.html", context)


def delete(request,id):
    """ delete the saved product and load favoris page"""

    f = Favoris.objects.filter(product_id=id, user=request.user)
    if f.exists():
        f.delete()

    product_list = Favoris.objects.filter(user=request.user)
    product = make_a_pagination(request, product_list)

    context = {
        "request": "favoris",
        "title": "mes aliments",
        "subtitle": "Retrouvez ici tous vos aliments préférés !",
        "product": product,
        "connected": request.user.is_authenticated,
        "paginate": True,
    }
    return render(request, "homepage/list.html", context)


@csrf_exempt
def save(request):
    """ add the product to the user favoris and
    return a json response to ajaxRequest"""

    data = json.loads(request.body)
    Favoris.objects.create(
        product_id=Product.objects.get(id=data["id"]), user=request.user
    )

    context = {"message": "favoris ajouté !"}

    return JsonResponse(context)


def legal(request):
    """ Simply load legal notice page """
    return render(request, "homepage/legal.html")
