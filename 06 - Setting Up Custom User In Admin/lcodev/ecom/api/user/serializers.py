from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes

from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # the instance is going to be interacting with the model and will be
        # saving it based on that
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = CustomUser
        # this is the point where we can add our extra parameter that we want to
        # be handled with the databases
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('name', 'email', 'password', 'phone',
                  'gender', 'is_active', 'is_stuff', 'is_superuser')
