from dataclasses import fields
from rest_framework import serializers
from ..models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        #fields = "__all__"
        exclude = ["watchlist"]


class WatchSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    wathclist = WatchSerializer(
        many=True, read_only=True)  # nested Serializers
    # wathclist = serializers.StringRelatedField(many=True)        # String Field
    # wathclist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # Primary Key Related
    # wathclist = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True, view_name="Watch-details")             # hyperlinked Related Field

    class Meta:
        model = StreamPlatform
        fields = "__all__"


# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('name is too short!')


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, valid_data):
#         return Movie.objects.create(**valid_data)

#     def update(self, instance, valid_data):
#         instance.name = valid_data.get('name', instance.name)
#         instance.description = valid_data.get(
#             'description', instance.description)
#         instance.active = valid_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'Title and Description should be the different!')
#         else:
#             return data

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('name is too short!')
    #     else:
    #         return value
