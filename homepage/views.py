from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

from django.http import HttpResponse


# PÁGINA INICIAL
def home(request):
    return render(request, 'homepage/home.html')



#Página registo ex2from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse

# Página Inicial
def home(request):
    return render(request, 'homepage/home.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso!")
            return redirect('login')  # Redireciona para a página de login após o registo
        else:
            messages.error(request, "Erro ao criar conta. Tente novamente.")
    else:
        form = UserCreationForm()
    return render(request, 'homepage/register.html', {'form': form})

# Página de Login
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial após login bem-sucedido
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")
            return render(request, 'login.html')
    return render(request, 'homepage/login.html')

#Página do Cart
def cart(request):
    # Aqui podes passar dados para o template se necessário
    return render(request, 'homepage/cart.html')