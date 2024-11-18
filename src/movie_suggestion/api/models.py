from datetime import timedelta
from django.utils import timezone

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from movie_suggestion.settings import TMDB_API_URL_IMAGE


class User(models.Model):
    name = models.CharField(u'Name', max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(u'e-mail', unique=True, db_index=True, max_length=80)
    birthday = models.DateField(u'Birthday')
    avatar = models.TextField(u'Avatar')
    password = models.CharField(max_length=128)
    createdAt = models.DateTimeField(db_index=True, auto_now_add=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def set_password(self, password):
        """Hashes the password and saves it to the password field."""
        self.password = make_password(password)

    def check_password(self, raw_password):
        """Checks if the provided password matches the stored hash."""
        return check_password(raw_password, self.password)

    def add_genre(self, genre):
        genre_user, created = GenresUser.objects.get_or_create(user=self, genre=genre)
        return created

    def remove_genre(self, genre):
        try:
            genre_user = GenresUser.objects.get(user=self, genre=genre)
            genre_user.delete()
            return True
        except GenresUser.DoesNotExist:
            return False


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)  # Setting `id` as primary key
    name = models.CharField('Genre', max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

    @classmethod
    def populate(cls, genres_list):
        # Check if the table is empty
        if not cls.objects.exists():
            # Table is empty, insert all genres
            genres_to_create = [cls(id=int(genre['id']), name=genre['name']) for genre in genres_list]
            cls.objects.bulk_create(genres_to_create)
        else:
            # Table is not empty, insert only missing genres
            existing_genre_ids = set(cls.objects.values_list('id', flat=True))
            existing_genre_names = set(cls.objects.values_list('name', flat=True))

            genres_to_create = [
                cls(id=genre['id'], name=genre['name'])
                for genre in genres_list
                if genre['id'] not in existing_genre_ids and genre['name'] not in existing_genre_names
            ]

            # Bulk create only the new genres if there are any
            if genres_to_create:
                cls.objects.bulk_create(genres_to_create)

        return f"{len(genres_to_create)} genres added."


class GenresUser(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('genre', 'user')


class MovieRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movieId = models.IntegerField()
    title = models.CharField(u'Title', max_length=50, null=False, blank=False)
    voteAverage = models.FloatField(u'Vote Average', null=False, blank=False, default=0.0)
    expireAt = models.DateTimeField(db_index=True, default=timezone.now() + timedelta(days=1))
    imageUrl = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_recommendation(self, user):
        return self.objects.filter(user=user, expireAt__gt=timezone.now()).first()

    @classmethod
    def add_recommendation(cls, user, movie):
        from ipdb import set_trace
        # set_trace()
        # Adds a recommendation if it doesn't already exist for the user, or returns the existing one if it's not
        # expired.
        movie_id = movie.get('id')
        title = movie.get('title')
        vote_average = movie.get('vote_average')
        image_url = f"{TMDB_API_URL_IMAGE}/{movie.get('poster_path')}"

        # Check if a recommendation exists and if it hasn't expired
        existing_recommendation = cls.objects.filter(user=user, movieId=movie_id).first()

        if existing_recommendation:
            if existing_recommendation.expireAt > timezone.now():  # Check if not expired
                return existing_recommendation  # Return the existing recommendation if it's not expired

        # Create and save a new recommendation
        recommendation = cls(
            user=user,
            movieId=movie_id,
            title=title,
            voteAverage=vote_average,
            expireAt=timezone.now() + timedelta(days=1),  # Set expiration to 1 day from now
            imageUrl=image_url
        )
        recommendation.save()
        return recommendation
