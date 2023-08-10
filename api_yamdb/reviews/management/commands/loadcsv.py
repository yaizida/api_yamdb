import csv

from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import (
    User,
    Category,
    Genre,
    Title,
    Review,
    Comment
)

FILE_PATH = 'static/data/'

data_to_load_csv = {
    'users': [
        User,
        [
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        ]
    ],
    'category': [
        Category,
        [
            'id',
            'name',
            'slug',
        ]
    ],
    'genre': [
        Genre,
        [
            'id',
            'name',
            'slug',
        ]
    ],
    'titles': [
        Title,
        [
            'id',
            'name',
            'year',
            'category_id',
        ]
    ],
    'genre_title': [
        Title.genre.through,
        [
            'id',
            'title_id',
            'genre_id',
        ]
    ],
    'review': [
        Review,
        [
            'id',
            'title_id',
            'text',
            'author_id',
            'score',
            'pub_date',
        ]
    ],
    'comments': [
        Comment,
        [
            'id',
            'review_id',
            'text',
            'author_id',
            'pub_date',
        ]
    ]
}


class Command(BaseCommand):
    help = '''Импортирует данные из CSV файлов в базу данных.
        Без указания файла импортирует все.'''

    def csv_load(self, file_name, model, fields):
        try:
            with open(f'{FILE_PATH}{file_name}.csv', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                objects = [
                    model(**dict(zip(fields, row)))
                    for row in reader
                ]
                model.objects.bulk_create(objects)
            self.stdout.write(self.style.SUCCESS(
                f'Данные из файла {file_name} загружены в базу данных.')
            )
        except IntegrityError as error:
            msg = f'Ошибка при записи данных из {file_name}.csv:{error}'
            raise IntegrityError(self.style.ERROR(msg))
        except FileNotFoundError as error:
            msg = (
                f'Файл {file_name}.csv не найден по пути {FILE_PATH}: {error}'
            )
            raise FileNotFoundError(self.style.ERROR(msg))
        except UnicodeDecodeError as error:
            msg = f'Ошибка при декодировании данных из {file_name}.csv:{error}'
            raise FileNotFoundError(self.style.ERROR(msg))

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_names',
            default=data_to_load_csv.keys(),
            type=str,
            nargs='*',
            help='''Названия CSV файлов, можно указать несколько.
                При указании файла следует следить,
                чтобы данные ссылались на существующий объект'''
        )

    def handle(self, *args, **options):
        for csv_name in options['csv_names']:
            data = data_to_load_csv[csv_name]
            self.csv_load(csv_name, *data)
