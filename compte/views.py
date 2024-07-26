from django.shortcuts import redirect, render
from django.contrib import messages

from compte.models import User
from django.contrib.auth import authenticate,login , logout
from django.core.mail import send_mail , EmailMessage

from django.conf import settings

from compte.utils import send_email_with_template

from  django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str

from .token import TokenGenerator
# pour recuperer le nom de domaine du site automatiquement
from django.contrib.sites.shortcuts import get_current_site

generate_token = TokenGenerator()
def user_registration_view(request,*args, **kwargs):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        passwordconfirm = request.POST.get('passwordconfirm')
        email = request.POST.get('email')
        if password != passwordconfirm:
            messages.error(request,'Les mots de passe ne correspondent pas')
            # pour verifier l'existence de user
        elif User.objects.filter(username=username).exists():
            messages.error(request, "ce nom d'utilisation existe déjà")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "cet email  existe déjà")
        else:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            
                                            email=email)
            user.save()

            # subject =  "Message de bienvenue"
            # message =  "Bienvenue sur notre site. {} {}.". format(user.first_name,user.last_name)
            to_email = user.email
            from_email = settings.EMAIL_HOST_USER
            template_name ='registration/activate_account.html'
            subject = 'Activation de compte'

            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)

            context = {
                'user': f"{user.first_name}{user.last_name}" ,
                'domain' :domain ,
                'uid' :uid ,
                'token' : token,

            }
            send_email_with_template(subject,template_name,context,[to_email],from_email)
            # to_email = user.email 
            # from_email = 'nossyandriamanalina050601@gmail.com'
            # send_mail(subject,message,from_email,[to_email],fail_silently=False)
            user.is_active = False

            messages.success(request, 'Votre compte a été crée avec succès')
    return render(request, 'registration/registration.html',{})

def user_login_view(request,*args, **kwargs):
    if request.method == "POST" :
          next = request.POST.get('next')
          print(next)
          username=request.POST.get('username')
          password=request.POST.get('password')
          user= User.objects.filter(username=username)
          if user.exists():
              if user.first().is_active :
                  user=authenticate(username=username, password=password)
                  if user is not None:
                      login(request,user)

                      messages.success(request,'vous etes connecté')

                      if next : 
                        return redirect(next)
                  else:
                      messages.error(request,"Le nom d'utilisateur ou le mot de passe est incorrect")
              else:
                  messages.error(request, "Votre compte n'est pas encore activé . Veuillez verifier votre boite email")
          else:
              messages.error(request,"Le nom d'utilisateur ou le mot de passe est incorrect")
    return render(request, 'registration/login.html', {})
      
                      # User is authenticated
          
def activate_account_view(request,uidb64,token,*args, **kwargs):
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
    
    return redirect('compte:connecter')
    # end try
# Create your views here.

# deconnexion 

def logout_view(request,*args, **kwargs):
    user = request.user
    # test permission
    if user.has_perm('compte.view_user_info'):
        print("user can view user info")
    
    if user.has_perms(['compte.view_user_info','compte.view_user_group']):
        print("user can view both")
    
    if user.is_student:
        print("user student")
    logout(request)
    
    
    messages.success(request,"vous etes deconnecté")
    return redirect('compte:connecter')