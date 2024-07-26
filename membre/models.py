from django.db import models


class UserWithFlotte(models.Model):
    '''Model definition for UserWithFlotte.'''
    user=models.OneToOneField("compte.User", on_delete=models.SET_NULL,null=True , blank=True)
    card=models.OneToOneField("card.Card", on_delete=models.SET_NULL,null=True, blank=True)
    custcode =  models.DecimalField(max_digits=10, decimal_places=2)
    type_de_ligne = models.CharField(max_length=50)
    plan_tarifaire = models.CharField(max_length=50)
    localisation = models.CharField(max_length=200)
    class Meta:
        '''Meta definition for UserWithFlotte.'''

        verbose_name = 'Information'
        verbose_name_plural = 'Informations'

    def __str__(self):
        return self.localisation
# Create your models here.
