
from django.urls import path



from pages import views


app_name = 'pages'
urlpatterns = [
    path("", views.home, name="home") ,
    path("connexion", views.connexion, name="connexion") ,
    path("deconnexion", views.deconnexion, name="deconnexion") ,
    path("inscription", views.inscription, name="inscription") ,
    path("forget_password", views.forget_password, name="forget_password") ,
    path("update_password", views.new_password, name="update_password") ,
    path("parametre", views.parametre, name="parametre") ,
    
    path("activate_account/<uidb64>/<token>/", views.activate_account, name="activate_account") ,
    path("reinitialiser_mdp/<uidb64>/<token>/", views.reinitialiser_mdp, name="reinitialiser_mdp") ,
    path("user_spec/<int:user_id>/", views.user_spec, name="user_spec") ,
    path("view_user", views.view_user, name="view_user") 
]