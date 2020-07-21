from django.conf.urls import url

from . import views

app_name = "homepage"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^create", views.create, name="create"),
    url(r"^account", views.account, name="account"),
    url(r"^login", views.login_user, name="login"),
    url(r"^logout", views.logout_user, name="logout"),
    url(r"^aliments/(?P<id>[0-9]+)/$", views.substituts, name="substituts"),
    url(r"^detail/(?P<id>[0-9]+)/$", views.detail, name="detail"),
    url(r"^search/", views.search, name="search"),
    url(r"^favoris/$", views.favoris, name="favoris"),
    url(r"^save/$", views.save, name="save"),
    url(r"^legal$", views.legal, name="legal"),
    url(r"^delete/(?P<id>[0-9]+)/$", views.delete, name="delete"),
    url(r"^update", views.update, name="update"),
    url(r"^pass", views.newpass, name="newpass"),
]
