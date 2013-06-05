import sys
import re
import tempfile
import hotshot
import hotshot.stats
from django.conf import settings
from cStringIO import StringIO


words_re = re.compile( r'\s+' )

group_prefix_re = [
    re.compile( "^.*/django/[^/]+" ),
    re.compile( "^(.*)/[^/]+$" ), # extract module path
    re.compile( ".*" ), # catch strange entries
]


class ProfileMiddleware(object):
    """
    Displays hotshot profiling for any view.
    http://yoursite.com/yourview/?prof

    Add the "prof" key to query string by appending ?prof (or &prof=)
    and you'll see the profiling results in your browser.
    It's set up to only be available in django's debug mode,
    but you really shouldn't add this middleware to any production
    configuration.
    * Only tested on Linux
    """

    def check_perms(self, request):
        return (settings.DEBUG or request.user.is_superuser) and 'prof' in request.GET

    def process_request(self, request):
        if self.check_perms(request):
            self.tmpfile = tempfile.mktemp()
            self.prof = hotshot.Profile(self.tmpfile)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.check_perms(request):
            return self.prof.runcall(callback, request, *callback_args,
                                     **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            self.prof.close()

            out = StringIO()
            old_stdout = sys.stdout
            sys.stdout = out

            stats = hotshot.stats.load(self.tmpfile)
            #stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats()

            sys.stdout = old_stdout
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                response.content = "<pre>" + stats_str + "</pre>"

        return response
