from django.contrib.auth.models import AbstractUser
from django.db import models
from . import datagen

class User(AbstractUser):
    pass

class Type(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length= 125)
    def __str__(self): return f" Type: {self.name}  "

class Schema(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user": self.user.id,
        }

    def get_column_names(self):
        return [
            field.name
            for field in self.fields.all()  # TODO:!!! order by fields.order
        ]

    def get_rows(self, number_of_rows):
        fields = list(self.fields.all())  # TODO: !!! order by fields.order

        rows = []
        for _ in range(number_of_rows):
            row = [
                field.generate_value()
                for field in fields
            ]
            rows.append(row)
        return rows

    def __str__(self): return f"schema {self.name}"

class Field(models.Model):
    name = models.CharField(max_length=25)
    _type = models.ForeignKey("Type", on_delete=models.CASCADE )
    order = models.PositiveSmallIntegerField(default = 1)#TODO : поменять default на более осмысленное и уникальное или убрать вовсе
    #_from = models.IntegerField()
    #_to = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type_id": self._type.id,
            "type_name": self._type.name,
            "type_description": self._type.description,
            "order": self.order
        }

    def __str__(self): return f" field: {self.name} | type: {self._type} "

class Schema_Field(models.Model):
    TYPE_FULL_NAME = 'FULL_NAME'
    TYPE_JOB = 'JOB'


    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name='fields',
    )
    field = models.ForeignKey("Field", on_delete=models.CASCADE)

    order = models.IntegerField()

    def __str__(self): return f" field: {self.field.name} of schema {self.schema.name} "


    def generate_value(self):
        if self.type == self.TYPE_FULL_NAME:
            return datagen.name_gen()
        elif self.type == self.TYPE_JOB:
            return datagen.job_gen()
        # Add more generators
        else:
            raise ValueError(f'No generator for field type "{self.type}"')

