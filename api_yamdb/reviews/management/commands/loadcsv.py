import csv

from django.core.management import BaseCommand

from reviews.models import (
    User,
    Category,
    Genre,
    Title,
    TitleGenre,
    Review,
    Comment
)

FILE_PATH = 'static/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{FILE_PATH}users.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                ).save()
            print('данные users.csv загруженны в базу данных')
        with open(f'{FILE_PATH}comments.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
            print('данные comments.csv загруженны в базу данных')
        with open(f'{FILE_PATH}genre.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Genre(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
            print('данные genre.csv загруженны в базу данных')
        with open(f'{FILE_PATH}titles.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category_id = Category.objects.get(id=row[3])
                Title(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category_id,
                ).save()
            print('данные title.csv загруженны в базу данных')
        with open(f'{FILE_PATH}genre_title.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                title_id = Title.objects.get(id=row[1])
                genre_id = Genre.objects.get(id=row[2])
                TitleGenre(
                    id=row[0],
                    title=title_id,
                    genre=genre_id,
                ).save()
            print('данные genre_title.csv загруженны в базу данных')
        with open(f'{FILE_PATH}review.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                author_id = User.objects.get(id=row[3])
                title_id = Title.objects.get(id=row[1])
                Review(
                    id=row[0],
                    author=author_id,
                    text=row[2],
                    pub_date=row[5],
                    title=title_id,
                    score=row[4],
                ).save()
            print('данные review.csv загруженны в базу данных')
        with open(f'{FILE_PATH}comments.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                author_id = User.objects.get(id=row[3])
                review_id = Review.objects.get(id=row[1])
                Comment(
                    id=row[0],
                    author=author_id,
                    text=row[2],
                    pub_date=row[4],
                    review=review_id,
                ).save()
            print('данные comments.csv загруженны в базу данных')
