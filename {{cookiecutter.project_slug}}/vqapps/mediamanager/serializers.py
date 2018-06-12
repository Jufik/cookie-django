from django.contrib.auth import get_user_model

from rest_framework import serializers

from vqapps.mediamanager.models import Media


class UserLightSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name'
        ]


class MediaSerializer(serializers.ModelSerializer):

    author = UserLightSerializer(read_only=True)

    def validate(self, data):
        if not data.get('image') and not data.get('attachment'):
            raise serializers.ValidationError("Vous devez saisir une image ou un fichier")
        if data.get('image') and data.get('attachment'):
            raise serializers.ValidationError("Vous devez saisir une image ou un fichier, et not les deux")
        return data


    class Meta:
        model = Media
        fields = [
            'id',
            'filename',
            'content_type',
            'attachment',
            'image',
            'author',
            'thumbnail_url',
            'rectangle_url',
            'created'
        ]


class MediaLightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = [
            'id',
            'filename',
            'content_type',
            'attachment',
            'image',
            'thumbnail_url',
            'rectangle_url',
            'created'
        ]
