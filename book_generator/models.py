from django.db import models
from book_generator.enums.book_jobs import BookJobs
from book_generator.enums.chapter_jobs import ChapterJobs

# better to use auth_user directly ?
# class User(models.Model):
#     class Meta:
#         # override default behaviour of django that adds the app name to the table
#         db_table = 'user'
#     name = models.CharField(max_length=50, blank=False)
#     email = models.CharField(max_length=50, blank=False)
#     password = models.CharField(max_length=50, blank=False) # Shall be encrypted,
#     role = models.Charfield(max_length=50, null=True, blank=True) # can be named permission. can be 'director', 'participant' or blank
#     active = models.BooleanField(default=false)


class Rule(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'rule'
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

class Book(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'book'
    number = models.IntegerField()
    title = models.CharField(max_length=100, null=True, blank=True)
    rounds = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

class BookPartaker(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'book_partaker'
        constraints = [models.UniqueConstraint(
            fields=['book', 'user', 'job'],
            name='unique_book_partaker_job'
        )]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    user = models.IntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE) #auth_user ?

    job = models.CharField(
        max_length=15,
        choices=[(job, job.value) for job in BookJobs]
    )

class BookRule(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'book_rule'
        constraints = [models.UniqueConstraint(
            fields=['book', 'rule'],
            name='unique_rule'
        )]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    author = models.ForeignKey(BookPartaker, on_delete=models.CASCADE)

class Chapter(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'chapter'

    number = models.IntegerField()
    title = models.CharField(max_length=100, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

class ChapterPartaker(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'chapter_partaker'
        constraints = [models.UniqueConstraint(
            fields=['chapter', 'user', 'job'],
            name='unique_chapter_partaker_job'
        )]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    user = models.IntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE) #auth_user ?

    job = models.CharField(
        max_length=15,
        choices=[(job, job.value) for job in ChapterJobs]
    )
