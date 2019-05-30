from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def signup_view(request):
    # a new user submitted a form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #log user in
            return redirect('app:index')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})
