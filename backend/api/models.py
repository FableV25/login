from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Note(models.Model):    
    title = models.CharField(
        max_length=100,
        blank=False,  
        null=False,   
        validators=[MinLengthValidator(1, message="El titulo no puede estar vacio")]
    )
    content = models.TextField(
        blank=False,  
        null=False,   
        validators=[MinLengthValidator(1, message="El contenido no puede estar vacio")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  