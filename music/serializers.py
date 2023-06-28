from rest_framework import serializers
from music.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','subscription_start','subscription_end')
