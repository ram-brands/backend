from .settings import *  # noqa: F401,F403

##############
# ADMIN SITE #
##############

PROJECT_NAME = "RAM Web Services"
MAIN_SITE_URL = "http://localhost:8080"


##################
# AUTHENTICATION #
##################

SIMPLE_JWT.update(  # noqa: F405
    {
        "SIGNING_KEY": "w8/L1-B-Bkov1;cs]mkvh*_6wW&./6m1:p89>.JFtTK$(dF9gn",
        "ALGORITHM": "HS256",
    }
)


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
    }
}


###############
# ENVIRONMENT #
###############

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


###########
# SECRETS #
###########

SECRET_KEY = "X.:IU=jrQLF+<uOBeh/ZK3vE4AaCL{.d;UO(g]>qV-w6sb:nfF"

AWS_ACCESS_KEY_ID = "AKIA4AWHNDASTGTJVSZA"
AWS_SECRET_ACCESS_KEY = "KnZB+StfliRAvr7TX283URDgprv0gZ+IHx8x6JW2"

AWS_REGION = "example-region"
RUNS_S3_BUCKET = "example-bucket"

AWS_LOCATION = "anonymous/"
