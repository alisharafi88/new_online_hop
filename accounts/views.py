from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, Value
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm

from .forms import CustomUserChangeForm


class ProfileView(LoginRequiredMixin, View):
    form_class = CustomUserChangeForm

    def get(self, request):
        user = request.user
        userprofile_form = self.form_class(instance=request.user)
        userpassword_form = PasswordChangeForm(request.user)
        orders = user.orders.prefetch_related('items').annotate(price=Sum(F('items__quantity') * F('items__price'))).all()
        return render(request, 'accounts/profile.html',
                      {'user': user, 'userprofile_form': userprofile_form, 'userpassword_form': userpassword_form, 'orders': orders})

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
