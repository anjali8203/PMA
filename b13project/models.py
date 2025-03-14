from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owned_projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='projects')
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    votes = models.IntegerField(default=0)  # for voting

    def __str__(self):
        return self.title
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vote_type = models.IntegerField(default=0) # +1 means upvote, -1 means downvote, 0 means no vote

    def __str__(self):
        return f"User: {self.user.first_name}, Project: {self.project.title}, Vote type: {self.vote_type}"

class JoinRequest(models.Model):
    project = models.ForeignKey(Project, related_name='join_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='join_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested to join {self.project.title}"


class UploadedFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url = models.URLField(max_length=1024)
    file_mime = models.TextField(max_length=64)
    file_type = models.TextField(max_length=16)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    keywords = models.CharField(max_length=255, default="")

    def keyword_list(self):
        """Returns the keywords as a list."""
        return self.keywords.split(",")


class Message(models.Model):
    project = models.ForeignKey(Project, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.author.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_joined = models.DateField(auto_now_add=True)
    interests = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    