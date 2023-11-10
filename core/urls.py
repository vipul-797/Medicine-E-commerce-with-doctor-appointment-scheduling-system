from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", views.index, name = "index"),
    path("login/", views.login, name = "login"),
    path("sign-up/", views.sign_up, name="sign_up"),
    #path("logout/", views.logout, name = "logout"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("disease-pred/", views.disease_pred, name="disease_pred"),
    path("drug-pred/", views.drug_pred, name="drug_pred"),
]