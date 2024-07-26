from django.db import models

class ImageUser(models.Model):
    '''Model definition for ImageUser.'''
    user=models.OneToOneField("compte.User", on_delete=models.SET_NULL , null=True)
    profil=models.ImageField( upload_to='profil_user', height_field=None, width_field=None, max_length=None , null=True)
    class Meta:
        '''Meta definition for ImageUser.'''

        verbose_name = 'ImageUser'
        verbose_name_plural = 'ImageUsers'

    def __str__(self):
        pass
# Create your models here.
