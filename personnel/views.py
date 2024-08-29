from mds import settings 
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as aut_login,logout as aut_logout
from django.core.mail import send_mail,EmailMessage
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
# from django.utils.encoding import force_bytes , force_text
from django.utils.encoding import force_bytes,force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from personnel.token import generatorToken
from personnel.models import Candidature, Affectation
from PIL import Image
from django.contrib.auth.views import LogoutView
import datetime



def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        username=request.POST['nameUser']
        password=request.POST['passwordUser']
        email=request.POST['emailUser']
        if User.objects.filter(username=username):
            messages.error(request,'ce nom a deja ete utilise')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request,'cet email a deja ete utilise')
            return redirect('register')
        if not username.isalnum():
            messages.error(request,"cet email a deja ete utilise")
            return redirect('register')
        prestataire=User.objects.create_user(username,email,password)
        prestataire.is_active = False
        prestataire.save()
        messages.success(request,'votre compte a ete cree avec succes allez verifiez votre email')
        current_site=get_current_site(request)
        email_subject = "confirmation de l'adresse email sur le systeme MDS"
        to_list=[prestataire.email]
        messageConfirm = render_to_string("emailconfirm.html",{
            "name":prestataire.username,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(prestataire.pk)),
            'token':generatorToken.make_token(prestataire)
        })
        email = EmailMessage(
            email_subject,messageConfirm,settings.EMAIL_HOST_USER,to_list,
        )
        email.fail_silently = False
        try:
            email.send()
        except Exception as e:
            print(f"Error: {e}")
    return render(request,'inscription.html')

def login(request):
    if request.method == 'POST':
        username=request.POST['nameUser']
        password=request.POST['passwordUser']
        prestataire = authenticate(username=username,password=password)
        if prestataire is not None:
            if prestataire.is_active == True:
                aut_login(request,prestataire)
                if request.user.is_staff:
                    messages.success(request,'vous etes connecte')
                    return redirect('/admin/')
                else:
                    try:
                        user = User.objects.get(username=username)
                        profil = Candidature.objects.get(user=user)
                        if profil is not None:
                            messages.success(request,"vous etes a present connecte a votre profil")
                            return redirect('candidature', profil.user.username)
                    except Candidature.DoesNotExist:
                        messages.success(request,'a present remplissez vos differentes informations')
                        return redirect('postuler')   
            else:
                messages.error(request,"vous n'avez pas confirme votre adresse email allez verifiez dans votre boite mail ")
        else:
            messages.error(request,'verifiez vos identifiants')
    return render(request,'connexion.html')

def custom_logout(request):
    aut_logout(request)
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        prestataire = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        prestataire = None
    if prestataire is not None and generatorToken.check_token(prestataire,token):
        prestataire.is_active = True
        prestataire.save()
        messages.success(request,'votre compte a ete bien active a present vous pouvez vous connecte')
        return redirect('login')
    else:
        messages.error(request,"veuillez activez votre compte")
 
@login_required
def postuler(request):
    if request.method == 'POST':
         user = request.user
         nom = request.POST.get('firstName')
         prenom = request.POST.get('lastName')
         email = user.email
         telephone = request.POST.get('phone')
         cni = request.POST.get('cni')
         localisation = request.POST.get('localisation')
         cv = request.FILES.get('cv')
         lettre_motivation = request.FILES.get('lettre_motivation')
         photo = request.FILES.get('photo')
         if photo:
            img = Image.open(photo)
            if img.width > 800 or img.height > 800:
                messages.error(request, "L'image doit être de 800x800 pixels ou moins.")
                return render(request, "postuler.html")
         candidature = Candidature(user=user,nom=nom,prenom=prenom,email=email,telephone=telephone,cni=cni,localisation=localisation,cv=cv,lettre_motivation=lettre_motivation,photo=photo)
         candidature.save()
         messages.success(request,'vos identifiants ont bien ete enregistres')
         return redirect('candidature', user.username)
    return render(request, "postuler.html")

@login_required   
def candidature(request, username):
    user = User.objects.get(username=username)
    profil = Candidature.objects.get(user=user)
    affectations = profil.affectation.all().order_by('-projet_id')
    if len(affectations) != 0:
        exp = True
    else:
        exp = False
    date = datetime.date(1999, 1, 1)
    last_affectation = profil.affectation.last()
    for affectation in affectations:
        if affectation.projet.date_fin > date:
            date = affectation.projet.date_fin
            last_affectation = affectation
            
    today = datetime.date.today()
    return render(request,'candidature.html',{"user":user, "profil":profil, 'affectations':affectations, 'today':today, 'last_affectation':last_affectation,'exp':exp})

def update(request, username):
    required= False
    user = User.objects.get(username=username)
    profil = Candidature.objects.get(user=user)
    if request.method == 'POST':
        profil.nom = request.POST.get('firstName')
        profil.prenom = request.POST.get('lastName')
        profil.email = user.email
        profil.telephone = request.POST.get('phone')
        profil.cni = request.POST.get('cni')
        profil.localisation = request.POST.get('localisation')
        if request.FILES.get('cv'):
            profil.cv = request.FILES.get('cv')
        if  request.FILES.get('lettre_motivation'):
            profil.lettre_motivation = request.FILES.get('lettre_motivation')
        if request.FILES.get('photo'):
            profil.photo = request.FILES.get('photo')
        if profil.photo:
            img = Image.open(profil.photo)
            if img.width > 800 or img.height > 800:
                messages.error(request, "L'image doit être de 800x800 pixels ou moins.")
                return render(request, "update.html" ,{"user":user,'profil':profil,'required':required})
        profil.save()
        try:
            messages.success(request,'vos informations ont bien ete mis a jour')
        except:
            messages.error("vos informations n'ont pas ete modifiees")
        return redirect('candidature',profil.user.username)
    return render(request,'update.html',{"user":user,'profil':profil,'required':required})
