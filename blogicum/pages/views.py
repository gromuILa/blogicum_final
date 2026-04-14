from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()


def about(request):
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    template = 'pages/rules.html'
    return render(request, template)


def csrf_error(request, exception):
    template = 'pages/403csrf.html'
    return render(request, template, status=403)


def page_not_found(request, exception):
    template = 'pages/404.html'
    return render(request, template, status=404)


def server_error(request):
    template = 'pages/500.html'
    return render(request, template, status=500)


@login_required
def edit_profile(request):
    template = 'pages/edit_profile.html'
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, template, context)
