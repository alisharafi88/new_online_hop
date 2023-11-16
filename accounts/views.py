from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm

from .forms import CustomUserChangeForm, AddressForm
from .models import UserAddress


class ProfileView(LoginRequiredMixin, View):
    form_class = CustomUserChangeForm

    def get(self, request):
        user = request.user
        userprofile_form = self.form_class(instance=request.user)
        userpassword_form = PasswordChangeForm(request.user)
        address = request.user.addresses.all()
        return render(request, 'accounts/profile.html',
                      {'user': user, 'address': address, 'userprofile_form': userprofile_form, 'userpassword_form': userpassword_form})

    def post(self, request):
        userprofile_form = self.form_class(request.POST, instance=request.user)
        if userprofile_form.is_valid():
            user = userprofile_form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, _('You Change your profile successfully!'), 'success')
            return redirect('accounts:profile')
        messages.error(request, userprofile_form.errors, 'danger')
        return redirect('accounts:profile')


class ChangePassword(LoginRequiredMixin, View):
    def Post(self, request):
        userpassword_form = PasswordChangeForm(request.user, request.POST)
        if userpassword_form.is_valid():
            userpassword_form.save()
            messages.success(request, _('You Change your profile successfully!'), 'success')
            return redirect('accounts:profile')
        messages.error(request, userpassword_form.errors, 'danger')
        print(userpassword_form.errors)
        return redirect('accounts:profile')


class ChangeAddress(LoginRequiredMixin, View):
    form_class = AddressForm

    def setup(self, request, *args, **kwargs):
        self.address = get_object_or_404(UserAddress, pk=kwargs['address_pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.address)
        return render(request, 'accounts/add_or_change_address.html', {'form': form, 'address': self.address})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.address)
        if form.is_valid():
            change_form = form.save(commit=False)
            change_form.user = request.user
            change_form.save()
            messages.success(request, _('You could change your address successfully.'), 'success')
            return redirect('accounts:profile')
        messages.error(request, _('You could NOT change your address.'), 'danger')
        return redirect(request.META.get('HTTP_REFERER', 'accounts:profile'))


class RemoveAddress(LoginRequiredMixin, View):
    def get(self, request, address_pk):
        get_object_or_404(UserAddress, pk=address_pk).delete()
        return redirect('accounts:profile')


class AddAddress(LoginRequiredMixin, View):
    form_class = AddressForm

    def get(self, request):
        return render(request, 'accounts/add_or_change_address.html', {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, _('You added your new address successfully.'), 'success')
            return redirect('accounts:profile')
        messages.error(request, form.errors, 'danger')
        return redirect(request.META.get('HTTP_REFERER', 'accounts:profile'))
