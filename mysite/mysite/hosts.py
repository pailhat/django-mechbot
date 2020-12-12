from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'mechbot', 'mechbot.urls', name='mechbot'),
    host(r'', 'mysite.urls', name='root'),   
)