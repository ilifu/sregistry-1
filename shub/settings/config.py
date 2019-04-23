'''

Copyright (C) 2017-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

# AUTHENTICATION

# Which social auths do you want to use?
ENABLE_GOOGLE_AUTH=False
ENABLE_TWITTER_AUTH=False
ENABLE_GITHUB_AUTH=True
ENABLE_GITLAB_AUTH=False
ENABLE_BITBUCKET_AUTH=False

# NOTE you will need to set autehtication methods up.
# Configuration goes into secrets.py
# see https://singularityhub.github.io/sregistry/install.html
# secrets.py.example provides a template to work from

# See below for additional authentication module, e.g. LDAP that are
# available, and configured, as plugins.



# DOMAIN NAMES

DOMAIN_NAME = "http://154.114.37.149"
DOMAIN_NAME_HTTP = "http://154.114.37.149"
DOMAIN_NAKED = DOMAIN_NAME_HTTP.replace('http://','')

ADMINS = (( 'jeremy', 'jeremy@idia.ac.za'),)
MANAGERS = ADMINS

HELP_CONTACT_EMAIL = 'jeremy@idia.ac.za'
HELP_INSTITUTION_SITE = 'https://docs.ilifu.ac.za'
REGISTRY_NAME = "ILIFU Computing Center"
REGISTRY_URI = "ilifu"



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
# - globus: allows connection from sregistry to endpoints
# - saml: authentication with SAML

PLUGINS_ENABLED = [
#    'ldap_auth',
#    'saml_auth'
]
