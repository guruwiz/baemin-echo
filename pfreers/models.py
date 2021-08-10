from django.db import models

# Create your models here.

class PfreeEateries(models.Model):
    KOREANFOOD = 'KF'
    SNACK = 'SN'
    CHICKEN = 'CH'
    PIZZA = 'PI'
    CHINESEFOOD = 'CF'
    FASTFOOD = "FF"
    BOSSAM = 'BO'
    HOTSOUP = 'HS'
    EATERY_TYPES_CHOICES = [
        (KOREANFOOD, 'Koreanfood'),
        (SNACK, 'Snack'),
        (CHICKEN, 'Chicken'),
        (PIZZA, 'Pizza'),
        (CHINESEFOOD, 'Chinesefood'),
        (FASTFOOD, "Fastfood"),
        (BOSSAM, 'Bossam'),
        (HOTSOUP, 'Hotsoup'), 
    ]
    eatery_types = models.CharField(max_length=2, choices=EATERY_TYPES_CHOICES, default='KOREANFOOD')
    def is_upperclass(self):
        return self.eatery_types in {self.KOREANFOOD, self.SNACK, self.CHICKEN, self.PIZZA, self.CHINESEFOOD, self.FASTFOOD, self.BOSSAM, self.HOTSOUP}
    eatery = models.CharField(max_length=50)
    echolv = models.CharField(max_length=10)
    echof_co_cnt = models.CharField(max_length=10)
    perf = models.CharField(max_length=10)
    create_date = models.DateTimeField()