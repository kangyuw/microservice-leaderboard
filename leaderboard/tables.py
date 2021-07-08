import django_tables2 as tables
from .models import Player

class PlayerTable(tables.Table):
    class Meta:
        model = Player
        template_name = "django_tables2/bootstrap.html"
        fields = ("username", "complete_time", "complete")