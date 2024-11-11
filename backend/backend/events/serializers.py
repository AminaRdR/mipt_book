from .models import Pair, EventType, EventItem, UserSearch
from rest_framework import serializers
import datetime


class PairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pair
        fields = ['name', 'time_slot_index', 'week_day_index', 'description']


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ['name', 'rules', 'description']


class UserSearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserSearch
        fields = ['data', 'owner_user_wallet', 'order_time']


class EventItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventItem
        fields = ['name', 'description', 'pair', 'owner_user_wallet', 'audience_number']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['pair'] = {
            'name': instance.pair.name,
            'time_slot_index': instance.pair.time_slot_index,
            'week_day_index': instance.pair.week_day_index,
            'description': instance.pair.description}
        # response['event_type'] = EventTypeSerializer(instance.event_type).data
        return response
