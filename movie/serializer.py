from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class movieSerializer(serializers.ModelSerializer):
    len_of_name = serializers.SerializerMethodField()
    moviePlatform=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Movie
        fields='__all__'
    def get_len_of_name(self,obj):
        return len(obj.name)
class streamPlatformSerializer(serializers.ModelSerializer):
    # nested serializers
    stream=movieSerializer(many=True, read_only=True)
    # string related field serializer
    # stream=serializers.StringRelatedField(many=True)
    # id
    # stream=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # with link
    # stream=serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie_detail'
    # )
    class Meta:
        model = StreamPlatform
        fields='__all__'
class reviewSerializer(serializers.ModelSerializer):
    review_movie = serializers.StringRelatedField(read_only=True)
    review_author=serializers.StringRelatedField(read_only=True)
    class Meta:
        model = review
        fields ='__all__'
# def field_length(value):
#     if len(value) < 2:
#         raise  serializers.ValidationError('name is too short')
# class movieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[field_length])
#     description = serializers.CharField()
#     active= serializers.BooleanField()
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
#     def update(self,instance,validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.active=validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('name sholdnot be equal description')
#         return data
#     def validate_name(self,value):
#         if len(value) < 2:
#             raise serializers.ValidationError('name too short')
#         return value
class userRegistration(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class  Meta:
        model = User
        fields = ('username','email','password','password2')
        extra_kwargs ={
            'password':{'write_only':True}
        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            return serializers.ValidationError({'errors':'password must be similar'})
        elif User.objects.filter(email=self.validated_data['email']).exists():
            return serializers.ValidationError({'errors':'email was tooken with another user'})
        else:
            account=User(email=self.validated_data['email'],username=self.validated_data['username'])
            account.set_password(password)
            account.save()
            return account