from portal.models import User
from rest_framework.serializers import ModelSerializer

class membersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','sir_name']