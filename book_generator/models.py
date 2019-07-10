from django.db import models
from django.conf import settings
from book_generator.enums.book_jobs import BookJobs
from book_generator.enums.chapter_jobs import ChapterJobs

class Rule(models.Model):
    class Meta:
        # override default behaviour of django that adds the app name to the table
        db_table = 'rule'
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def getAllFields(self):
        return '"' + self.name + '" is active' if self.active else ''

class Book(models.Model):
    class Meta:
        db_table = 'book'
    number = models.IntegerField()
    title = models.CharField(max_length=100, null=True, blank=True)
    rounds = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.number + '. ' + self.title

class BookPartaker(models.Model):
    class Meta:
        db_table = 'book_partaker'
        constraints = [models.UniqueConstraint(
            fields=['book', 'user', 'job'],
            name='unique_book_partaker_job'
        )]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.CharField(
        max_length=15,
        choices=[(job, job.value) for job in BookJobs]
    )

    def __str__(self):
        return (self.book.number + '. ' + self.book.title + '. '
            + self.user.username + ' as ' + self.job)

class BookRule(models.Model):
    class Meta:
        db_table = 'book_rule'
        constraints = [models.UniqueConstraint(
            fields=['book', 'rule'],
            name='unique_rule'
        )]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    author = models.ForeignKey(BookPartaker, on_delete=models.CASCADE)

    def __str__(self):
        return (self.book.number + '. ' + self.book.title + '. ' + self.rule.name
            + ' is ' + self.description + '. By ' + self.author.username)

class Chapter(models.Model):
    class Meta:
        db_table = 'chapter'

    number = models.IntegerField()
    title = models.CharField(max_length=100, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.number + '. ' + self.title

class ChapterPartaker(models.Model):
    class Meta:
        db_table = 'chapter_partaker'
        constraints = [models.UniqueConstraint(
            fields=['chapter', 'user', 'job'],
            name='unique_chapter_partaker_job'
        )]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.CharField(
        max_length=15,
        choices=[(job, job.value) for job in ChapterJobs]
    )

    def __str__(self):
        return (self.chapter.number + '. ' + self.chapter.title + '. '
            + self.user.username + ' as ' + self.job)
