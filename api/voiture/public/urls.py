from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import home, image_upload,signup,profile,voiture,cle,garage
from .forms import MyLoginView

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view() ,name="logout"),
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
    path("voiture/", voiture, name="voiture"),
    path("garage/", garage, name="garage"),
    path("cle/", cle, name= "cle"),
    path("upload", image_upload, name="upload"),

]