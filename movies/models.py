from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
    TYPES = (
        ('movie', 'MOVIE'),
        ('serie', 'SERIE')
    )

    id = models.AutoField(primary_key=True, help_text="Unique ID to identify a movie or a serie")
    name = models.CharField(max_length=500, null=False)
    genre = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPES, default='movie', help_text='Type')
    visualizations = models.PositiveIntegerField(default=0)
    qty_score = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0,
        validators=[
            MaxValueValidator(5.0, message="El valor debe ser menor o igual a 5."),
            MinValueValidator(0.0, message="El valor debe ser mayor o igual a 1.")
        ]
    )


    def __str__(self):
        txt = '{0}. Nombre: {1}, Género: {2}'
        return txt.format(self.id, self.name, self.genre)


class UserInteraction(models.Model):
    user = models.CharField(max_length=200) #username
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    visualization = models.BooleanField(default=False)
    score = models.BooleanField(default=False)
