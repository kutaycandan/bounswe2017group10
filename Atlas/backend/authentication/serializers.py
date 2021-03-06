from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers
from rest_framework_jwt import serializers as jwt_serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = (
            'id', 'email', 'username', 'date_created', 'date_modified',
            'firstname', 'lastname', 'password', 'confirm_password')
        read_only_fields = ('date_created', 'date_modified')

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username',
                                               instance.username)
        instance.firstname = validated_data.get('firstname',
                                                instance.firstname)
        instance.lastname = validated_data.get('lastname',
                                               instance.lastname)

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and password == confirm_password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, data):

        email = data['email']
        #Ensure email exists
        if not email:
            raise serializers.ValidationError('Users must have a valid e-mail address')
        password = data['password']
        #Ensure password consists of at least 1 capital letter, digit and 7 chars
        if not (any(x.isupper() for x in password) and any(x.isdigit() for x in password) and len(password) >= 7):
            raise serializers.ValidationError('Password should contain at least one capital letter and digit and 7 chars.')
        '''
            Ensure the passwords are the same
        '''
        if data['password']:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError(
                    "The passwords have to be the same"
                )
        return data

class CustomJWTSerializer(jwt_serializers.JSONWebTokenSerializer):
    username_field = 'username_or_email'
    def validate(self, attrs):

        password = attrs.get("password")
        user_obj = Account.objects.filter(email=attrs.get("username_or_email")).first() or Account.objects.filter(username=attrs.get("username_or_email")).first()
        if user_obj is not None:
            credentials = {
                'username':user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_serializers.jwt_payload_handler(user)

                    return {
                        'token': jwt_serializers.jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)