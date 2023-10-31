from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import CustomUser, UserAddress
from .forms import CustomUserChangeForm


class ProfileView(View):
    def get(self, request):
        user_form = CustomUserChangeForm(instance=request.user)
        address = request.user.addresses.all()
        return render(request, 'accounts/profile.html', {'user': request.user, 'address': address, 'user_form': user_form})

    def post(self, request):
        user_form = CustomUserChangeForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, _('You Change your profile successfully!'), 'success')
            return redirect('accounts:profile')
        # messages.error(request, _('Somthing WRONG happened, Try again!'), 'danger')
        # return redirect('accounts:profile')


class ChangePassword(View):
    def Post(self, request):
        pass
