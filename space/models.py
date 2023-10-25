from django.db import models

from core_auth.models import User


# Create your models here.


class ConferenceHall(models.Model):

    customer = models.ForeignKey(User,  on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    price = models.PositiveIntegerField()

    Capacity = models.PositiveIntegerField()

    description = models.CharField(max_length=50)

    image = models.ImageField(upload_to='images/space/hall')

    is_available = models.BooleanField(default=False)

    location = models.TextField()


    def is_date_available(self, date):

        bookings = ConferenceBooking.objects.filter(

            space=self,

            start_date__lte=date,
            end_date__gte=date
        )

        return not bool(bookings)


    def __str__(self):

        return self.name
    




class CoWorkSpace(models.Model):

    customer = models.ForeignKey(User,  on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    price = models.PositiveIntegerField()

    slots = models.PositiveIntegerField()

    description = models.CharField(max_length=50)

    image = models.ImageField(upload_to='images/space/hall')

    is_available = models.BooleanField(default=False)

    location = models.TextField()


    def is_date_available(self, date):

        bookings = CoWorkBooking.objects.filter(

            space=self,

            start_date__lte=date,
            end_date__gte=date
        )

        return not bool(bookings)


    def __str__(self):

        return self.name




class CoWorkBooking(models.Model):

    space = models.ForeignKey(CoWorkSpace, on_delete=models.CASCADE)  

    start_date = models.DateField()

    end_date = models.DateField()


    def __str__(self):

        return f"Booking for {self.space} by {self.customer}"



class ConferenceBooking(models.Model):

    space = models.ForeignKey(ConferenceHall, on_delete=models.CASCADE)  

    start_date = models.DateField()

    end_date = models.DateField()


    def __str__(self):

        return f"Booking for {self.space} by {self.customer}"