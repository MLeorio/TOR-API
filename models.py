from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime

class Annonce(models.Model):
    id = fields.IntField(pk=True)
    libelle_objet = fields.CharField(max_length=250)
    description_objet = fields.TextField()
    image_of_object = fields.TextField()
    first_name_person_to_contact = fields.CharField(max_length=255, null=True)
    last_name_person_to_contact = fields.CharField(max_length=255, null=True)
    telephone_person_to_contact = fields.CharField(max_length=12)
    place_of_loss_or_find = fields.CharField(max_length=255)
    date_of_loss_or_find = fields.DateField()
    

    statut = fields.CharField(max_length=50, ) # Statut de l'annonce (soit trouver ou perdu)
    actif = fields.IntField(default=1) # avertit si l'annonce est toujours actif ou pas (l'objet a retrouve son propretaire) 1=Oui 0=Non


    created_at = fields.DatetimeField(auto_now_add=True, default=datetime.now())
    updated_at = fields.DatetimeField(auto_now=True, default=datetime.now())

    def __str__(self):
        return self.libelle_objet



class Device(models.Model):
    id = fields.BigIntField(pk=True)
    device_id = fields.CharField(max_length=255)
    installation_date = fields.DatetimeField(auto_now_add=True, default=datetime.now())




Annonce_Pydantic = pydantic_model_creator(Annonce, name="Annonce")
AnnonceIn_Pydantic = pydantic_model_creator(Annonce, name="AnnonceIn", exclude_readonly=True)

Device_Pydantic = pydantic_model_creator(Device, name="Device")
DeviceIn_Pydantic = pydantic_model_creator(Device, name="DeviceIn", exclude_readonly=True)