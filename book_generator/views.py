from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the Book Generator. You can start a new Exquisite Corpse Book here.")
