from django.contrib.auth.models import AbstractUser
from django.db import models
from . import datagen, fields_types

class User(AbstractUser):
    pass


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
    order = models.PositiveSmallIntegerField(default = 1, null=True, blank=True)#TODO : поменять default на более осмысленное и уникальное или убрать вовсе
    kind = models.CharField(
        max_length=64,
        choices=fields_types.type_choice,
        default="Temporary Type" #TODO: разобраться с : поменять default или

    )

    def generate_value(self):
        if self.kind == fields_types.TYPE_FULL_NAME:
            return datagen.name_gen()
        elif self.kind == fields_types.TYPE_JOB:
            return datagen.job_gen()
        # Add more generators
        else:
            raise ValueError(f'No generator for field type "{self.kind}"')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
        }

    def __str__(self): return f" field: {self.name} | type: {self.kind} "

class Schema_Field(models.Model):

    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name='fields',
    )
    field = models.ForeignKey("Field", on_delete=models.CASCADE)

    #order = models.IntegerField()

    def __str__(self): return f" field: {self.field.name} of schema {self.schema.name} "

