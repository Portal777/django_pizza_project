from django.conf import settings
from django.forms import models
from rest_framework import serializers
from .models import Pizza, Topping


class ToppingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return Topping.objects.create(**validated_data)


class PizzaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=50)
    image = serializers.ImageField(read_only=True)
    author_id = serializers.IntegerField()
    recipe = ToppingSerializer(many=True, read_only=True)

    # recipe = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Topping.objects.all())

    def create(self, validated_data):
        return Pizza.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.id = validated_data.get('id', instance.id)
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.slug = validated_data.get('slug', instance.slug)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.author_id = validated_data.get('author_id', instance.author_id)
    #     instance.recipe = validated_data.get('recipe', instance.recipe)
    #     instance.save()
    #
    #     return instance