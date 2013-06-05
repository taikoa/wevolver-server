from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = u'category'

    def __unicode__(self):
        return u'%s' % self.name
