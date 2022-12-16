from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from application import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generateToken
# Create your views here.


def home(request, *args, **kwargs):
    return render(request, 'authentification/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        if User.objects.filter(username=username):
            messages.error(request, 'Ce surnom existe deja,utiliser un autre')
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, 'Ce email a deja un compte')
            return redirect('signup')


        if not username.isalnum():
            messages.error(request, ' Le surnom doit etre alphanumerique')
            return redirect('signup')

        if password != confirmpwd:
            messages.error(request, 'Confirmation de mots de passe incorrecte')
            return redirect('signup')                  

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.success(request, 'Votre compte à été créé avec succès. nous vous avons envoyé un e-mail Vous devez confirmer afin activer votre compte.')
# send email when account has been created successfully
        subject = "Bienvenu sur ODCB authentification"
        message = "Bienvenu "+ my_user.first_name + " " + my_user.last_name + "\n merci d'avoir choisi ODCB ,pour vous connectez.\n confirmé votre email pour ci-dessus \n merci"
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

# send the the confirmation email
        current_site = get_current_site(request) 
        email_suject = "confirme ton email de ODCB pour vous connectez!"
        messageConfirm = render_to_string("emailConfimation.html", {
            'name': my_user.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generateToken.make_token(my_user)
        })       

        email = EmailMessage(
            email_suject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [my_user.email]
        )

        email.fail_silently = False
        email.send()
        return redirect('signin')
    return render(request, 'authentification/signup.html')    


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)


        if user is not None:
            login(request, user)
            return redirect('verification')



        elif my_user.is_active == False:
            messages.error(request, 'Vous n avez pas encore confirmer votre email pour activer votre compte.')
            return redirect('signin')

        else:
            messages.error(request, 'bad authentification')
            return redirect('home')
    return render(request, 'authentification/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Deconnexion reussie')
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active  = True
        my_user.save()
        messages.success(request, "Votre compte a été activé ,vous pouvez maintenant vous connectez!")
        return redirect("signin")
    else:
        messages.success(request, 'Activation echoué ,veuillez reprendre')
        return redirect('home')
def admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']


        if (username=="admin" and password=="admin"):

            return render(request, 'authentification/add.html')




    return render(request, 'authentification/add.html')