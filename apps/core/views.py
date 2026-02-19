from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def about(request):
    try:
        return render(request, "core/about.html")
    except Exception as e:
        return render(request, "core/about.html", {"error": str(e)})