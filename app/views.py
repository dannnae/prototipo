from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        user_logged_in = True
    else:
        user_logged_in = False

    usuario = request.user

    context = {'user_logged_in': user_logged_in, 'usuario': usuario}
    return render(request, "index.html", context)