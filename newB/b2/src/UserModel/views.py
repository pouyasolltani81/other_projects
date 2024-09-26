from django.shortcuts import render
from django.views.generic import ListView


from .models import User

class UsersListView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        return context
