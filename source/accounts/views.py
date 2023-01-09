from django.views.generic import CreateView
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from .form import MyUserCreationForm


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'sign_in.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:product_index')
        return next_url