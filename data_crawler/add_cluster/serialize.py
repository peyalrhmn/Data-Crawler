from django.db import models
from django.db.models import fields
from rest_framework import serializers
from add_cluster.models import Create_cluster

class Create_cluster_serialize(serializers.ModelSerializer):
    class Meta:
        model = Create_cluster
        fields = "__all__"