from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/registration_form.html', context)
