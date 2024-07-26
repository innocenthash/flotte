from django.db import models
from django.urls import reverse

class Card(models.Model):
    '''Model definition for Card.'''
    msisdn = models.IntegerField()
    number_sim = models.IntegerField()
    puk = models.IntegerField()
    class Meta:
        '''Meta definition for Card.'''

        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return str(self.number_sim)
    
    def get_admin_url(self):
        return reverse('admin:card_card_change', args=[self.pk])