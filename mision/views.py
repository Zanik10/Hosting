from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Task
from .models import Puntos_usuario, Historial_misiones
from django.shortcuts import get_object_or_404
# Create your views here.



def home(request):
    return render(request, 'home.html')

def mapa(request):
    return render(request, 'mapa.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])    
                user.save() #Esto hace que se guarde directo en la base de datos :D
                login(request, user)
                return redirect('misiones')
            
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Ya existe manito'
                })
        return render(request, 'signup.html', {
            'form' : UserCreationForm,
            'error' : 'Las contraseñas no coinciden'
        })
    
def misiones(request):
    listar_misiones = Task.objects.all()
    return render(request, 'misiones.html', {'listar_misiones': listar_misiones})

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form' : AuthenticationForm,
                'error': 'El usuario o la contraseña esta incorrecta'
            })
        else:
            login(request, user)
            return redirect('misiones')


def misiones(request):
    if request.user.is_authenticated:
        listar_misiones = Task.objects.all()
        puntos_usuario = Puntos_usuario.objects.get_or_create(usuario=request.user)[0]
        context = {'listar_misiones': listar_misiones, 'puntos_usuario': puntos_usuario.puntos}
        return render(request, 'misiones.html', context)
    else:
        listar_misiones = Task.objects.all()
        return render(request, 'misiones.html', {'listar_misiones': listar_misiones})

def sumar_puntos(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    # Aquí deberías obtener el usuario actual
    usuario_actual = request.user
    
    try:
        # Intenta obtener el objeto Puntos_usuario para el usuario actual
        puntos_usuario = Puntos_usuario.objects.get(usuario=usuario_actual)
    except Puntos_usuario.DoesNotExist:
        # Si el objeto no existe, crea uno nuevo con los puntos de la tarea
        puntos_usuario = Puntos_usuario.objects.create(usuario=usuario_actual, puntos=task.puntos)
    
    # Suma los puntos al usuario
    puntos_usuario.puntos += task.puntos
    puntos_usuario.save()
    
    # Registra la misión en el historial
    Historial_misiones.objects.create(mision=task, usuario=usuario_actual)
    
    
    return redirect('misiones')

def ranking(request):
    usuarios_con_puntos = Puntos_usuario.objects.all().order_by('-puntos')
    print("Usuarios con puntos:", usuarios_con_puntos)

    top_10_usuarios = usuarios_con_puntos[:10]
    otros_usuarios = usuarios_con_puntos[10:]

    # Obtener la posición del usuario autenticado
    usuario_autenticado = request.user
    posicion_usuario_autenticado = None

    if usuario_autenticado.is_authenticated:
    # Obtener el índice del usuario autenticado en la lista ordenada
        try:
            posicion_usuario_autenticado = [u.usuario.id for u in usuarios_con_puntos].index(usuario_autenticado.id)
            print("Posición del usuario autenticado:", posicion_usuario_autenticado)
        except ValueError:
            posicion_usuario_autenticado = None

    return render(request, 'ranking.html', {
        'top_10_usuarios': top_10_usuarios,
        'otros_usuarios': otros_usuarios,
        'posicion_usuario_autenticado': posicion_usuario_autenticado,
        'usuario_autenticado': usuario_autenticado,
    })



def home(request):
    if request.user.is_authenticated:
        puntos_usuario = Puntos_usuario.objects.get_or_create(usuario=request.user)[0]
        context = {'puntos_usuario': puntos_usuario.puntos}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
    