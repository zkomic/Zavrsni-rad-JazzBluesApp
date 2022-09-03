from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout
from accounts.forms import registrationForm, addFields
from django.contrib.auth.decorators import login_required
from JazzBluesApp.models import Users
from django.contrib import messages

def register(request): 
    if request.method == "POST":
        u_form = registrationForm(request.POST)
        p_form = addFields(request.POST, request.FILES)
        print('osnovna', u_form.errors)
        print('gender i slika', p_form.errors)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()#dohvacanje podataka iz UserCreationForm-a
            details = p_form.save(commit=False)#dohvacanje podataka iz forme sa gender i slikom
            details.user=user#postavljanje usera iz UserCreationForm u korisnika
            details.save()
            return redirect ('accounts:login')
    else:
        u_form = registrationForm()
        p_form = addFields()
    return render(request, 'register.html', {'u_form':u_form, 'p_form':p_form})


def login_fun(request): 
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)#validacija podataka
        if form.is_valid():
            next_url = request.POST.get('next_url')
            #log in the user
            user = form.get_user()#dohvacanje upisanih podataka (usera)
            login(request, user)#logiranje usera
            return redirect ('home')
        else:
            messages.warning(request, "Login error!") 
            context = {
            'form': AuthenticationForm(),
        }
    else:
        context = {
            'form': AuthenticationForm(),
        }
    return render(request, 'login.html', context)

@login_required
def logout_fun(request):
    logout(request)
    return redirect('home')