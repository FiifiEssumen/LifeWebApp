from rest_framework import serializers
from Slife.models import Category, Option


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name",'slug','details','views']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields =["name","votes"]

