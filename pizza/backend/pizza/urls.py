from django.urls import path, include
from . import views


app_name = 'pizza'

urlpatterns = [
    path('', views.index, name='index'),
    path('pizza/make_pizza/', views.make_pizza, name='make_pizza'),
    path('pizza/make_topping/', views.make_topping, name='make_topping'),
    path('pizza/<slug>/', views.pizza, name='pizza'),
    path('toppings/', views.topping_filter, name='topping_filter'),
    path('api/v1/pizza/', views.PizzaView.as_view()),
    path('api/v1/pizza/<int:pk>', views.PizzaView.as_view()),
    path('api/v1/topping/', views.ToppingView.as_view()),
    path('api/v1/topping/<int:pk>', views.ToppingView.as_view()),
]

