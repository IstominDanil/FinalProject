from django.forms import Select
from django_filters import FilterSet, ModelChoiceFilter
from .models import Advertisement, Reply


# Создаем функцию-запрос, которая возвращает все объявления пользователя
def my_ads_requests(request):
    if request is None:
        return Advertisement.objects.none()

    return Advertisement.objects.filter(author=request.user)


# Создаем свой набор фильтров для модели Reply.
class ReplyFilter(FilterSet):
    # поиск по объявлению
    final = ModelChoiceFilter(
        queryset=my_ads_requests,
        empty_label='Все объявления',
        label='',
        widget=Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Reply
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = [
            'final',
        ]