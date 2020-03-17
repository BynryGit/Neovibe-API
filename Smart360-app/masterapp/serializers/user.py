import jwt
from rest_framework import serializers
from masterapp.models.user_lookup import Privilege
from smart360_API.settings import SECRET_KEY
from userapp.models.user import User


class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilege
        fields = ('id_string','name', 'description')

class CreatePrivilegeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    id_string = serializers.CharField(required=False)
    # token = serializers.CharField(required=True)

    class Meta:
        model = Privilege
        fields = ('id_string','name', 'description')

    def create(self, validated_data, token):
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id_string=data['id_string'])
        if Privilege.objects.filter(name=validated_data['name']).exists():
            return False
        else:
            privilege = Privilege()
            privilege.name = validated_data['name']
            privilege.description = validated_data['description']
            privilege.created_by = user
            privilege.save()
            return True

    def update(self, validated_data, token):
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id_string=data['id_string'])
        if Privilege.objects.filter(id_string=validated_data['id_string'],is_deleted=False).exists():
            privilege = Privilege.objects.get(id_string=validated_data['id_string'],is_deleted=False)
            privilege.name = validated_data['name']
            privilege.description = validated_data['description']
            privilege.updated_by = user
            privilege.save()
            return True
        else:
            return False

    def delete(self, validated_data):
        if Privilege.objects.filter(id_string=validated_data['id_string'],is_deleted=False).exists():
            privilege = Privilege.objects.get(id_string=validated_data['id_string'],is_deleted=False)
            privilege.is_deleted=True
            privilege.save()
            return True
        else:
            return False