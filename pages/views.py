import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from compte.models import ImageUser, User
from django.contrib.auth import authenticate,login , logout
from django.conf import settings
from  django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from compte.token import TokenGenerator
from compte.utils import send_email_with_template
# pour recuperer le nom de domaine du site automatiquement
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required , permission_required
from .forms import ImageUserForm
from django.views.decorators.csrf import csrf_exempt
generate_token = TokenGenerator()
def base(request,*args, **kwargs):
    template_name = 'base.html'
   
    return render(request, template_name, {})

@login_required(login_url='pages:connexion')
def home(request,*args, **kwargs):
    template_name = 'home.html'
    users= User.objects.all()
    context = {
        'users':users
    }
    return render(request,template_name,context)
def connexion(request,*args, **kwargs):
    template_name = 'connexion.html' 
    context ={
               
                'email': ' ',
                
                'password': ' ',
                
    }  
    if request.method=='POST' :
        next = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.exists():
            if user.first().is_active:
                user = authenticate(request, username=username , password=password)
                if user is not None:
                    login(request,user)

                   
                    messages.success(request, 'Vous etes connecté')
                    if next : 
                        return redirect(next)
                    else:
                        return redirect('pages:home')
                else:
                 
                    messages.error(request,"Le nom d'utilisateur ou le mot de passe est incorrect")
            else:
                messages.error(request, "Votre compte n'est pas encore activé, Veuillez verifier votre boite email")
        else :
            messages.error(request, 'Votre adresse email est incorect')
   
    return render(request, template_name, {})
def inscription(request,*args, **kwargs):
    template_nam = 'inscription.html' 
    context ={
                'username': ' ',
                'email': ' ',
                'first_name': '',
                'last_name': '',
                'password': '',
                'password_repeat': ''
    }  
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        if password != password_repeat:
            messages.error(request,'Le mot de passe ne correspondent pas')
        elif User.objects.filter(username=username).exists():
            messages.error(request,"ce nom d'utilisateur existe déjà")
        elif User.objects.filter( email=email).exists():
            messages.error(request,"cette adresse email existe déjà")
        else:
            user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
            user.is_active = False
            user.save()
            # envoie mail après inscription
            to_email = user.email
            from_email = settings.EMAIL_HOST_USER
            template_name = 'mail_activate_account.html'
            subject = "Activation de compte"
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            context = {
                'user': f"{user.first_name} {user.last_name}",
                'domain' :domain ,
                'uid' :uid ,
                'token' : token,

            }
            
            if send_email_with_template(subject, template_name, context, [to_email], from_email):
                messages.success(request, 'Votre compte a été créé avec succès.Veuillez consulter votre adresse email pour activer votre compte.')
            else:
                messages.error(request, 'Erreur lors de l\'envoi de l\'email') 
            
    return render(request, template_nam, context)
def activate_account(request,uidb64,token,*args, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'votre compte a été activé avec succès')
    else:
        messages.error(request,"Le lien d'activation est invalide")
    
    return redirect('pages:connexion')
# end def
def deconnexion(request,*args, **kwargs):
    
    logout(request)
    
    
    messages.success(request,"vous etes deconnecté")
    return redirect('pages:connexion')

def forget_password(request,*args, **kwargs):
    template_name = 'forget_password.html' 
    if request.method=="POST":
        email = request.POST.get('email')
        user_recup = User.objects.filter(email=email)
        if user_recup.exists():
            for user in user_recup:
                  # envoie mail après inscription
                  to_email = user.email
                  from_email = settings.EMAIL_HOST_USER
                  template_nam = 'mail_reinitialisation_mdp.html'
                  subject = "Reinitialisation de mot de passe"
                  domain = get_current_site(request).domain
                  uid = urlsafe_base64_encode(force_bytes(user.pk))
                  token = generate_token.make_token(user)
                  context = {
                      'user': f"{user.first_name} {user.last_name}",
                       'domain' :domain ,
                       'uid' :uid ,
                       'token' : token,

                      }
                  if send_email_with_template(subject, template_nam, context, [to_email], from_email):
                      messages.success(request, 'Veuillez consulter votre adresse email pour reinitialiser votre mot de passe')
                  else:
                      messages.error(request, 'Erreur lors de l\'envoi de l\'email') 
        else:
            messages.error(request,"Votre adresse email est incorrect")  
    return render(request, template_name, {})

def reinitialiser_mdp(request,uidb64,token,*args, **kwargs):
    template_name = "reinitialiser_mdp.html"
    if request.method == "POST":
        try:
           uid = force_str(urlsafe_base64_decode(uidb64))
           user = User.objects.get(pk=uid)
           password = request.POST.get('password')
           confirm_password = request.POST.get('confirm_password')
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
           user = None
        if user is not None and generate_token.check_token(user,token):
            if password == confirm_password :
               user.set_password(password)
               user.save()
               messages.success(request,'votre mot de passe a été reinitialiser avec succès')
            else:
               messages.error(request,'votre mot de passe ne sont pas identique')     
        else:
           messages.error(request,"Le lien d'activation est invalide") 
    return render(request, template_name, {})

@login_required(login_url='pages:connexion')
def parametre(request,*args, **kwargs):
    template_name = "parametre.html"
    imageuser_instance, created = ImageUser.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ImageUserForm(request.POST, request.FILES, instance=imageuser_instance)
        if form.is_valid():
            form.save()
            form.fields['profil'].initial = None
            # messages.success(request, 'Votre profil a été mis à jour avec succès')
            return redirect('pages:parametre')
    else:
        form = ImageUserForm(instance=imageuser_instance)
    
    return render(request, template_name, {'form': form})
# end def
def new_password(request,*args, **kwargs):
    template_name = 'update_password.html'  
    return render(request, template_name, {})

# @csrf_exempt  user_spec
def view_user(request,*args, **kwargs):
    """
    Purpose: 
    """
    data = json.loads(request.body)
    return JsonResponse(data,safe=False)
def user_spec(request,user_id,*args, **kwargs):
    """
    Purpose: 
    """
    template_name = 'view_spec.html'  
    user = User.objects.filter(id=user_id).first()
    context = {
        'user':user
    }
    return render(request, template_name,context)
# end def
# Create your views here.
