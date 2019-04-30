'''

Copyright (C) 2017-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''
from os import getenv
from ast import literal_eval

# AUTHENTICATION

# Which social auths do you want to use?
ENABLE_GOOGLE_AUTH=getenv("ENABLE_GOOGLE_AUTH", default='False').lower() == 'true'
ENABLE_TWITTER_AUTH=getenv("ENABLE_TWITTER_AUTH", default='False').lower() == 'true'
ENABLE_GITHUB_AUTH=getenv("ENABLE_GITHUB_AUTH", default='False').lower() == 'true'
ENABLE_GITLAB_AUTH=getenv("ENABLE_GITLAB_AUTH", default='False').lower() == 'true'
ENABLE_BITBUCKET_AUTH=getenv("ENABLE_BITBUCKET_AUTH", default='False').lower() == 'true'

# NOTE you will need to set autehtication methods up.
# Configuration goes into secrets.py
# see https://singularityhub.github.io/sregistry/install.html
# secrets.py.example provides a template to work from

# See below for additional authentication module, e.g. LDAP that are
# available, and configured, as plugins.



# DOMAIN NAMES
ENV_DOMAIN_NAME=getenv('DOMAIN_NAME', default='127.0.0.1')
DOMAIN_NAME = f'http://{ENV_DOMAIN_NAME}'
DOMAIN_NAME_HTTP = f'http://{ENV_DOMAIN_NAME}'
DOMAIN_NAKED = DOMAIN_NAME_HTTP.replace('http://','')

ADMINS = literal_eval(getenv('ADMINS', default='(("someone", "someone@yourdomain.com"), )'))  # (( 'dane', 'kennedy.dane@gmail.com`'),)
MANAGERS = ADMINS

HELP_CONTACT_EMAIL = getenv('HELP_CONTACT_EMAIL')
HELP_INSTITUTION_SITE = getenv('HELP_INSTITUTION_SITE')
REGISTRY_NAME = getenv('REGISTRY_NAME')
REGISTRY_URI = getenv('REGISTRY_URI')



# PERMISSIONS

# Allow users to create public collections
USER_COLLECTIONS = True

# Should registries by default be private, with no option for public?
PRIVATE_ONLY = False

# Should the default for a new registry be private or public?
DEFAULT_PRIVATE = False


# DATABASE

# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Visualizations

# After how many single containers should we switch to showing collections
# only? >= 1000
VISUALIZATION_TREEMAP_COLLECTION_SWITCH=1000


# Logging

# Do you want to save complete response metadata per each pull?
# If you disable, we still keep track of collection pull counts, but not specific versions
LOGGING_SAVE_RESPONSES=True

# Plugins
# Add the name of a plugin under shub.plugins here to enable it



# Available Plugins:

# - ldap_auth: Allows sregistry to authenitcate against an LDAP directory
# - pam_auth: Allow users from (docker) host to log in
# - globus: allows connection from sregistry to endpoints
# - saml: authentication with SAML

PLUGINS_ENABLED = [
#    'ldap_auth',
#    'pam_auth',
#    'globus',
#    'saml_auth'
]
