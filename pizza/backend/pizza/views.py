from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from .models import Pizza, Topping
from .forms import MakePizzaForm, MakeToppingForm
from transliterate import translit, slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import PizzaSerializer, ToppingSerializer

# Create your views here.

def index(request):
    pizza = Pizza.objects.all()
    toppings = Topping.objects.all()

    content = {
        'pizza': pizza,
        'toppings': toppings,
    }
    return render(request, 'pizza/index.html', context=content)


def pizza(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)

    content = {
        'pizza_image': pizza.image,
        'pizza_name': pizza.title,
        'toppings': pizza.recipe.all,
        'author': pizza.author
    }

    return render(request, 'pizza/pizza.html', content)


def make_pizza(request):
    if request.method == "POST":
        form = MakePizzaForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(translit(request.POST.get('title'), 'ru'))
            post.save()
            form.save_m2m()  # сохраняем связанную таблицу

            return redirect('pizza:pizza', slug=post.slug)

        else:
            content = {
                'error': 'Произошла ошибка добавления данных',
            }
            return render(request, 'pizza/make_pizza.html', content)

    content = {
        'form': MakePizzaForm()
    }
    return render(request, 'pizza/make_pizza.html', content)


def make_topping(request):
    if request.method == "POST":
        form = MakeToppingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('pizza:index')

        else:
            content = {
                'error': 'Произошла ошибка добавления данных',
            }
            return render(request, 'pizza/make_topping.html', content)

    content = {
        'form': MakeToppingForm()
    }
    return render(request, 'pizza/make_topping.html', content)


def topping_filter(request):
    if request.method == "GET":
        topping = request.GET.get('topping_name')
        pizzas = None
        if topping:
            use_topping = get_object_or_404(Topping, title=topping)
            pizzas = Pizza.objects.filter(recipe=use_topping.id)
        context = {
            "toppings": Topping.objects.all(),
            "topping": topping,
            "pizzas": pizzas,
        }
        return render(request, "pizza/topping_filter.html", context=context)


class PizzaView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pizza = Pizza.objects.all()
        if pk:
            pizza = Pizza.objects.filter(pk=pk)

        serializer = PizzaSerializer(pizza, many=True)
        return Response({"pizza": serializer.data})

    def post(self, request):
        pizza = request.data.get('pizza')
        serializer = PizzaSerializer(data=pizza)
        if serializer.is_valid(raise_exception=True):
            pizza_saved = serializer.save()
        return Response({'success': f'Pizza {pizza_saved.title} created successfully'})

    def delete(self, request, pk):
        pizza = get_object_or_404(Pizza.objects.all(), pk=pk)
        pizza.delete()
        return Response({"message": f"Pizza with id `{pk}` has been deleted."}, status=204)

    # def put(self, request, pk):
    #     saved_pizza = get_object_or_404(Pizza.objects.all(), pk=pk)
    #     data = request.data.get('pizza')
    #     serializer = PizzaSerializer(instance=saved_pizza, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         pizza_saved = serializer.save()
    #     return Response({"success": "Pizza '{}' updated successfully".format(pizza_saved.title)})


class ToppingView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        topping = Topping.objects.all()
        if pk:
            topping = Topping.objects.filter(pk=pk)

        serializer = ToppingSerializer(topping, many=True)
        return Response({"topping": serializer.data})

    def post(self, request):
        topping = request.data.get('topping')
        serializer = ToppingSerializer(data=topping)
        if serializer.is_valid(raise_exception=True):
            topping_saved = serializer.save()
        return Response({'success': f'Topping {topping_saved.title} created successfully'})

    def delete(self, request, pk):
        topping = get_object_or_404(Topping.objects.all(), pk=pk)
        topping.delete()
        return Response({"message": f"Topping with id `{pk}` has been deleted."}, status=204)
