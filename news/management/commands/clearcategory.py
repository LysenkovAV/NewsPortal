from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Deleting all posts of the selected category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you want to delete all posts in a category {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Cancelled'))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(categories=category).delete()
            # в случае неправильного подтверждения говорим, что в доступе отказано
            self.stdout.write(self.style.SUCCESS(f"Succesfully deleted all news from category {category.name}"))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category'))
