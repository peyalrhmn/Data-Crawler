from django.db import models

# Create your models here.

class Create_cluster(models.Model):
    cluster_name = models.CharField(max_length=50)
    depth = models.IntegerField()
    strategy = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    url = models.CharField(max_length=250)
    class Meta:
        db_table = "clusters"
        
#class Search_cluster(models.Model):
#    cluster_name = models.CharField(max_length=50)
#    url = models.CharField(max_length=250)
#    data = models.TextField()
#    class Meta:
#        db_table = "data"
