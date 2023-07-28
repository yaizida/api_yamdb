from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator
# from rest_framework.exceptions import ValidationError

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
