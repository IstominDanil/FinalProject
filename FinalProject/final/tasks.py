import datetime

from celery import shared_task

from django.conf import settings
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives


from .models import Advertisement, Category, Reply


# функция отправки уведомлений подписчикам на почту о новом объявлении в любимой категории
def subscribers_send_mails(pk, headline, subscribers_emails):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'mail/adv_add_email.html',
        {
            'link': f'{settings.SITE_URL}/final/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject=headline,
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=subscribers_emails,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


# функция отправки на почту автору объявления уведомления о том, что у него есть новый отклик
def ad_author_send_mail(pk, email):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'mail/reply_add_email.html',
        {
            'link': f'{settings.SITE_URL}/final/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject='Новый отклик',
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


# функция отправки на почту автору оклика уведомления о том, что его отклик принят
def reply_author_send_mail(pk, email):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'mail/reply_approve_email.html',
        {
            'link': f'{settings.SITE_URL}/final/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject='Отклик принят',
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)


# задача, которая уведомляет о новом объявлении в любимом разделе
@shared_task
def adv_add_notification(pk):
    adv = Advertisement.objects.get(id=pk)
    category = adv.category
    subscribers = []
    subscribers_emails = []
    subscribers += category.subscribers.all()

    for s in subscribers:
        subscribers_emails.append(s.email)

    subscribers_send_mails(final.pk, final.headline, subscribers_emails)


# задача, которая уведомляет о новом отклике на объявление
@shared_task
def reply_add_notification(pk):
    reply = Reply.objects.get(id=pk)
    final = reply.adv
    final_author_email = [final.author.email]
    final_author_send_mail(final.pk, final_author_email)


# задача, которая уведомляет о принятом отклике
@shared_task
def reply_approve_notification(pk):
    reply = Reply.objects.get(id=pk)
    adv = reply.adv
    reply_author_email = [reply.user.email]
    reply_author_send_mail(final.pk, reply_author_email)


# задача по еженедельной отправке сообщения подписчикам со списком новых объявлений за неделю
# из категорий, на которые они подписаны
@shared_task
def my_job():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    ads = Advertisement.objects.filter(created_at__gte=week_ago)
    categories = set(final.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'mail/weekly_final.html',
        {
            'link': settings.SITE_URL,
            'final': final
        }
    )
    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=False)