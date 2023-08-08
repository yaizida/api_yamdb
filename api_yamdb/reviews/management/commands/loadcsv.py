import csv

from django.db import connection
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

FILE_PATH = 'static/data/'

data_to_load_csv = {
    'users':
    """
    INSERT INTO reviews_user
    (id,username,email,role,bio,first_name,last_name,password,is_superuser,is_staff,is_active,date_joined)
    VALUES (%s, %s, %s, %s, %s, %s, %s, '', '', '', '', '')
    """,
    'category':
    """
    INSERT INTO reviews_category (id,name,slug)
    VALUES (%s, %s, %s)
    """,
    'genre':
    """
    INSERT INTO reviews_genre (id,name,slug)
    VALUES (%s, %s, %s)
    """,
    'titles':
    """
    INSERT INTO reviews_title (id,name,year,category_id)
    VALUES (%s, %s, %s, %s)
    """,
    'genre_title':
    """
    INSERT INTO reviews_title_genre (id,title_id,genre_id)
    VALUES (%s, %s, %s)
    """,
    'review':
    """
    INSERT INTO reviews_review (id,title_id,text,author_id,score,pub_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    'comments':
    """
    INSERT INTO reviews_comment (id,review_id,text,author_id,pub_date)
    VALUES (%s, %s, %s, %s, %s)
    """,
}


class Command(BaseCommand):
    help = '''Импортирует данные из CSV файлов в базу данных.
        Без указания файла импортирует все.'''

    def csv_load(self, file_name):
        try:
            with open(f'{FILE_PATH}{file_name}.csv', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                data = []
                for row in reader:
                    data.append(row)
                with connection.cursor() as cursor:
                    cursor.executemany(
                        data_to_load_csv[file_name],
                        data
                    )
                    connection.commit()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные из файла {file_name}.csv успешно записанны'
                    )
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
            self.csv_load(csv_name)
