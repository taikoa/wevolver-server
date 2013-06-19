from django.conf import settings

PROJECT_APPS = (
        'wevolve.projects',
        'wevolve.project_parts',
        'wevolve.tasks',
        'wevolve.users'
        )

INSTALLED_APPS = settings.INSTALLED_APPS + ('django_jenkins', 'django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'wevolve_test',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
