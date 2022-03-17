from django.db import models

# Create your models here.

class Customer(models.Model ):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female') )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.IntegerField()
    salary = models.IntegerField()

    def __str__(self):
            return self.gender

class Diabetes(models.Model ):
    pregnancies = models.IntegerField(null=False, blank= False)
    glucose = models.IntegerField(null=False, blank= False)
    bloodPressure = models.IntegerField(null=False, blank= False)
    skinThickness = models.IntegerField(null=False, blank= False)
    insulin = models.IntegerField(null=False, blank= False)
    bmi = models.DecimalField(null=False, blank= False, decimal_places=1, max_digits=3)
    diabetesPedigreeFunction = models.DecimalField(null=False, blank= False, decimal_places=3, max_digits=4)
    age = models.IntegerField(null=False, blank= False)

    # def __str__(self):
    #         return self.gender
