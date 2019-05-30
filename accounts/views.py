from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: log user in
            return redirect('app:index')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
