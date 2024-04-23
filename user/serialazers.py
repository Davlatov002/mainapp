from rest_framework import serializers
from .models import Profile, Transaction, Identified, MoneyOut

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfilesingupSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password','mac_address']

class Tranzaktionserialazer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['profile_id', 'balance_usdt','balance_netbo', 'created_at']

class UserTranzaktionserialazer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['balance_usdt','balance_netbo', 'created_at']

class ProfileRefeleshSerialazer(serializers.Serializer):
    referal_link = serializers.CharField()

class ProfileLoginserialazer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class VerificationCodeserialazer(serializers.Serializer):
    code = serializers.CharField()
    
class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'surname', 'profile_image']

    def update(self, instance, validated_data):
        # Update each field individually
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()

        return instance
    
class UpdateEmPsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email', 'password']

    def update(self, instance, validated_data):
        # Update each field individually
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
                                                                
        return instance

class GMProfileserialazer(serializers.Serializer):
    email = serializers.EmailField()

class IdentifiedSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Identified
        fields = '__all__'

class CreatMoneyOutserialazer(serializers.Serializer):
    wallet_addres = serializers.CharField()
    balance_netbo = serializers.FloatField()

class MoneyOutserialazer(serializers.ModelSerializer):
    class Meta:
        model = MoneyOut
        fields = '__all__'

class IdentifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identified
        fields = fields = ["fullname", "birthday", "serial_document", "id_image", "address_image", "selfie_image"]