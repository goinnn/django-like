import datetime

from optparse import make_option
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('-u', '--num-users', default=10000, dest='num_users',
                    help='Min num the users'),
            make_option('-q', '--num-queries', default=10000, dest='num_queries',
                    help='Min num the queries'),
    )
    help = "Benchmark between queries with like and regex"

    def handle(self, **options):
        num_users = int(options.get('num_users'))
        num_queries = int(options.get('num_queries'))
        print 'Creating data...'
        self.initial()
        print 'Queries with like'
        time_like = self.berkmar_like(use_like=True, num_queries=num_queries)
        print time_like
        print 'Queries with regex'
        time_regex = self.berkmar_like(use_like=False, num_queries=num_queries)
        print time_regex
        improvement = (100 * float(time_regex.seconds - time_like.seconds) / time_like.seconds)
        print "Improvement: %s %%" % improvement

    def initial(self, num_users=10000):
        if num_users < User.objects.all().count():
            print 'The data was created'
            return
        for i in range(num_users):
            User.objects.get_or_create(username='user %s' %i)

    def berkmar_like(self, use_like=False, num_queries=10000):
        datetime_initial = None
        User.objects.count()

        for i in range(num_queries):
            if i == 0:
                datetime_initial = datetime.datetime.now()
            if use_like:
                list(User.objects.filter(username__like='u%%%s' % i))
            else:
                list(User.objects.filter(username__regex='^u.*%s$' % i))
            if i == num_queries - 1:
                time = datetime.datetime.now() - datetime_initial
        return time
