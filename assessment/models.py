from django.db import models

class Submission(models.Model):
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=32)
    profession = models.CharField(max_length=128)
    scenario = models.TextField()
    answers = models.JSONField()  # {"q1": "...", "q2": "..."}
    scores = models.JSONField()   # {"overall": 75, "self_awareness": 80, ...}
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profession} - {self.created_at:%Y-%m-%d %H:%M}"
