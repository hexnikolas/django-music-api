from django.db import models


# Artist model
class Artist(models.Model):
    GENRE_CHOICES = [
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Metal', 'Metal'),
        ('Indie', 'Indie'),
        ('House', 'House'),
        ('Techno', 'Techno'),
    ]
    name = models.CharField(max_length=100, primary_key=True)
    short_description = models.TextField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    class Meta:
        db_table = "artist"
    def __str__(self):
        return self.name

# Album model
class Album(models.Model):
    ALBUM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('EP', 'EP'),
        ('Album', 'Album'),
    ]
    name = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=20, choices=ALBUM_TYPE_CHOICES)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "album"
    def __str__(self):
        return self.name

# Track model
class Track(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    lyrics = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=5)  # Assuming format: MM:SS
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    class Meta:
        db_table = "track"
    def __str__(self):
        return self.title

# user model
class User(models.Model):
    subscription_start = models.DateField(blank=True, null=True)
    subscription_end = models.DateField(blank=True, null=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = "user"
    def __str__(self):
        return str(user_id)
