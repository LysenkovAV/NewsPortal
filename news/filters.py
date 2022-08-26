from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Category


class PostFilter(FilterSet):
    time_add_search = DateTimeFilter(
        field_name='time_add',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

    # Для организации поиска по списку категорий постов
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        conjoined=False,  # поиск по принципу ИЛИ
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],  # для организации поиска по названию
        }
