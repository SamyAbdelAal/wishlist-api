from rest_framework import serializers
from items.models import  Item, FavoriteItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			]

class ItemListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name = "api-detail",
		lookup_field = "id",
		lookup_url_kwarg = "item_id"
		)
	added_by=UserSerializer()
	favorite_count=serializers.SerializerMethodField()
	class Meta:
		model = Item
		fields = [
			'id',
			'image',
			'name',
			'description',
			'added_by',
			'favorite_count',
			'detail',
			]
	def get_favorite_count(self,obj):
		favorite = obj.favoriteitem_set.count()
		return favorite

class FavoriteSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	class Meta:
		model = FavoriteItem
		fields = [
			'user',
			]


class ItemDetailSerializer(serializers.ModelSerializer):
	favorite_by= serializers.SerializerMethodField()
	added_by=UserSerializer()
	class Meta:
		model = Item
		fields = [
			'id',
			'image',
			'name',
			'description',
			'added_by',
			'favorite_by',
			]
	def get_favorite_by(self,obj):
		favorite = obj.favoriteitem_set.all()
		return FavoriteSerializer(favorite, many=True).data


