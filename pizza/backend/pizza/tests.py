# импорты для работы тестов
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainapp.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainapp.settings")
import backend.mainapp.wsgi

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Pizza, Topping





class PizzaTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='tests')
        topping1 = Topping.objects.create(title='Тестовый топпинг1')
        topping2 = Topping.objects.create(title='Тестовый топпинг2')

        self.pizza = Pizza.objects.create(
            author=user,
            title='Тестовая1',
            description='Тестовая пицца 1',
            slug='testovaya1',
        )

        self.pizza.recipe.add(topping1.id)
        # self.pizza.recipe.add(topping2.id)

    def test_valid_pizza(self):
        self.assertTrue(len(self.pizza.return_recipe().all()) > 0)
        self.assertTrue(self.pizza.is_valid_pizza())

    def test_invalid_pizza(self):
        self.pizza.title = ''
        self.pizza.save()
        self.assertFalse(self.pizza.is_valid_pizza())

    def test_pizza_api_post(self):
        csrf_client = Client(enforce_csrf_checks=True)
        c = Client()
        c.login(username='test', password='12345')

        response = c.get("/api/v1/pizza/1")
        print(response.content)
        print(response.status_code)

        data = {
                        "title": "Апишная2",
                        "description": "Пицца созданная с помощью api",
                        "slug": "apishnaya2",
                        "author_id": 1
                }

        response = c.post("/api/v1/pizza/", data=data)
        print(response.content)
        self.assertEqual(response.status_code, 201)
        try:
            print(Pizza.objects.get(slug='apishnaya'))
        except Pizza.DoesNotExist:
            print('Нет объекта с таким ключом')
