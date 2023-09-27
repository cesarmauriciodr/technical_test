"""
This file contains the settings for the project.
"""

# set the default storage options
STORAGE_OPTIONS = (
    ('local', 'Local'),
    ('s3', 'Amazon S3'),
    ('google', 'Google cloud storage'),
    ('azure', 'Google BIgQuery'),
)
# set the default storage option
STORAGE = 'local'

# set the default debug option
DEBUG = True

# set the default storage option path
if STORAGE == 'local':
    PATH_LOCAL = 'data/'
elif STORAGE == 's3':
    BUCKET_NAME = 'netflix-titles'
elif STORAGE == 'google':
    BUCKET_NAME = 'netflix_titles'
elif STORAGE == 'bigquery':
    BUCKET_NAME = 'netflix_titles'

# set the default file name
FILE_NAME = 'netflix_titles.csv'

UPLOAD_FOLDER = 'data_files'

#flask secret key
SECRET_KEY = 'secret key'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['csv', 'txt', ])

APP_PORT = 5000
APP_HOST = '0.0.0.0'
