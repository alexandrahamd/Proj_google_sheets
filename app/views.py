from django.views.generic import ListView

from app.models import Order


class AppView(ListView):
    model = Order
    template_name = 'app/order_list.html'
