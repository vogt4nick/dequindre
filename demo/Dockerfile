FROM continuumio/miniconda3:latest

LABEL description = "Creates image to run ci-dequindre demo"
LABEL maintainer = "nick.vogt@dynatrace.com"

# ----------------------------------------------------------------------------
# Extra installs
# ----------------------------------------------------------------------------

# install necessary locales
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen 

# dos2unix for fixing line endings and other stuff
RUN apt-get update && apt-get install -y dos2unix

# ----------------------------------------------------------------------------
# Environment Variables
# ----------------------------------------------------------------------------

ENV HOMEDIR /opt/demo
RUN mkdir -p ${HOMEDIR}

# ----------------------------------------------------------------------------
# Setup image directory
# ----------------------------------------------------------------------------

COPY ./packages ${HOMEDIR}/packages
COPY ./conda-envs ${HOMEDIR}/conda-envs
COPY ./schedules ${HOMEDIR}/schedules
COPY ./tasks/ ${HOMEDIR}/tasks

# fix windows line endings 
RUN find ${HOMEDIR} -name *.sh | xargs chmod +x
RUN find ${HOMEDIR} -name *.sh | xargs dos2unix
RUN find ${HOMEDIR} -name *.py | xargs chmod +x
RUN find ${HOMEDIR} -name *.py | xargs dos2unix

# ----------------------------------------------------------------------------
# Setup Conda Environments
# ----------------------------------------------------------------------------

# create every environment
RUN . ${HOMEDIR}/conda-envs/setup-conda-envs.sh

# ENTRYPOINT [ "python", "opt/demo/schedules/demo.py" ]
