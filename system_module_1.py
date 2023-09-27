import os
import pandas as pd
import settings
import logging


class DataIngestion:
    """
    Data ingestion class
    """

    def __init__(self, file_path):
        """
        Initialize the class.
        
        Args:
            file_path (str): Path of the file to ingest.
        """
        self.file_path = file_path

        # Determine the storage type and perform ingestion accordingly
        if settings.STORAGE == 'local':
            self.ingest_to_local()
        elif settings.STORAGE == 's3':
            self.ingest_to_s3()
        elif settings.STORAGE == 'google':
            self.ingest_to_gcs()
        elif settings.STORAGE == 'bigquery':
            self.ingest_to_bigquery()

    def ingest_logger(func):
        """
        Decorator to log the ingestion process. ion a file
        """
        def wrapper(*args, **kwargs):
            logging.basicConfig(filename='ingestion.log', level=logging.INFO)
            logging.info(f'Ingestion started for {args[0].file_path}')
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f'Error while ingesting {args[0].file_path} to {settings.STORAGE}')
                logging.error(f'Error while ingesting {args[0].file_path} to {settings.STORAGE}')
            print(f'Ingestion completed')
            logging.info(f'Ingestion completed for {args[0].file_path}')
        return wrapper

    @ingest_logger
    def ingest_to_gcs(self):
        """
        Load CSV to Google Cloud Storage and return the path.
        """
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.BUCKET_NAME)
        blob = bucket.blob(settings.FILE_NAME)
        blob.upload_from_filename(self.file_path)
        return f'gs://{settings.BUCKET_NAME}/{settings.FILE_NAME}'

    @ingest_logger
    def ingest_to_local(self):
        """
        Load CSV to local file system.
        """
        df = pd.read_csv(self.file_path)
        df.to_csv(os.path.join(settings.PATH_LOCAL, settings.FILE_NAME))

    @ingest_logger
    def ingest_to_s3(self):
        """
        Load CSV to Amazon S3.
        """
        pass  # Add your S3 ingestion logic here

    @ingest_logger
    def ingest_to_bigquery(self):
        """
        Load CSV to BigQuery.
        """
        pass  # Add your BigQuery ingestion logic here

    def get_path(self):
        """
        Get the path of the file.
        """
        if settings.STORAGE == 'local':
            return os.path.join(settings.PATH_LOCAL, settings.FILE_NAME)
        elif settings.STORAGE == 's3':
            return f's3://{settings.BUCKET_NAME}/{settings.FILE_NAME}'
        elif settings.STORAGE == 'google':
            return f'gs://{settings.BUCKET_NAME}/{settings.FILE_NAME}'
        elif settings.STORAGE == 'bigquery':
            return f'bigquery://{settings.BUCKET_NAME}/{settings.FILE_NAME}'

    def allowed_file(self, filename):
        """
        Check if the file type is allowed.
        
        Args:
            filename (str): Name of the file.
        
        Returns:
            bool: True if the file type is allowed, False otherwise.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


if __name__ == '__main__':
    """
    This script runs the Flask app using Gunicorn or in debug mode.
    """
    from app import app  # Import the Flask app
    import gunicorn  # Import Gunicorn for production deployment
    import settings  # Import the settings module for configuration
    
    if settings.DEBUG:
        # Run the app in debug mode
        app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)
    else:
        # Use Gunicorn for production deployment
        gunicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)