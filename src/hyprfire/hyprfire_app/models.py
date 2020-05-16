from django.db import models
#from django.contrib.postgres.fields import ArrayField


class Data(models.Model):
    """
    This is a class model for the Django ORM.
    The class Data will store the filename, alogirthm, window_size, analysis and csv_data into the database
    using Django's inbuilt ORM libraries.

    Primary Key: is "id" set Django's default primary key if not listed. Auto increment.
    filename: the filepath/name
    algorithm: Either Zipf or Benford
    window_size = the size of window (an integer)
    analysis = The type of analysis to do: Time or Length
    data = the csv data, contains 4 types of data. timestamp, uvalue, start_epoch, end_epoch.
    """

    filename = models.TextField()
    algorithm = models.TextField()
    window_size = models.IntegerField()
    analysis = models.TextField()
    #data = ArrayField(models.TextField())
