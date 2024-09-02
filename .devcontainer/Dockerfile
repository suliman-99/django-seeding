FROM python:3.10.14-bookworm
WORKDIR /app

# Set environment variables to avoid prompts during package installations
# caso não dê certo, voltar `&& export DEBIAN_FRONTEND=noninteractive \`
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
    && apt-get purge -y imagemagick imagemagick-6-common

RUN python3 -m pip install --upgrade \
    setuptools==69.0.3 \
    gitpython==3.1.41

# django-seeding specifics
RUN pip install pipenv
RUN apt-get install -y sqlite3 libsqlite3-dev

# finalizing..
RUN apt-get clean
