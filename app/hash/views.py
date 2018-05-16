from .forms import HashForm
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
import requests
from bs4 import BeautifulSoup
from django_cron import CronJobBase, Schedule
from .models import Hash
from django.core.mail import send_mail
import datetime, time

class ThanksPageView(TemplateView):
    template_name = "thanks.html"


class HtmlParse:
    def __init__(self, hash_=None):
        self.hash_ = hash_

    def get_url(self):
            return 'https://blockchain.info/tx/' + self.hash_.value

    def get_content_page(self):
        link = self.get_url()
        if link:
            return requests.get(link).content

    def get_parsed_data(self):
        data = self.get_content_page()
        if data:
            soup = BeautifulSoup(data, "lxml")
            table = soup.find_all('table', attrs={'class': 'table table-striped'})[1]
            rows = table.find_all('td')
            count_str = str(rows[9]).split()[0]
            confirmation_count = count_str.split('>')[1]
            print(confirmation_count)
            if confirmation_count.isdigit():
                self.hash_.is_confirmed = True
                self.hash_.save()
            #else:
                #self.hash_.is_confirmed = False ???
                #self.hash_.save() ??? or
                #
            pass


def home(request):
    if request.method == 'POST':
        form = HashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = HashForm()
    return render(request, 'base.html', {'form': form})


class MailSender:
    def __init__(self, hash_):
        self.text = "Your transaction confirmed"
        self.from_ = "info.example.com"
        self.notification = 'Notification'
        self.hash_ = hash_

    def send_email(self):
        send_mail(
            self.notification,
            self.text,
            self.from_,
            ['dekamiron@yandex.ru'],
            #[self.hash_.user_email],  # to
            fail_silently=False,
        )


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'hash.views.MyCronJob'

    def do(self):
        print("work")
        unconfirmed_transactions = list(Hash.objects.filter(is_confirmed=False))
        #unconfirmed_transactions = list(Hash.objects.filter(is_confirmed=True))
        print(unconfirmed_transactions)
        for unconfirmed_transaction in unconfirmed_transactions:
            parser = HtmlParse(unconfirmed_transaction)
            print('checking') #проверить получение объекта
            parser.get_parsed_data()
            print('sending  email')
            try:
                post_man = MailSender(unconfirmed_transaction)
                post_man.send_email()
            except Exception as e:
                print(e)
            print('sent')
        print('close')
