from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ["id", "title", "url", "poster", "poster_id", "created", "votes"]

    def get_votes(self, post):
        return Votes.objects.filter(posts=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ["id"]
