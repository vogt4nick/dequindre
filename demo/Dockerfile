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
ENV HOME /opt
ENV CONDA_DIR ${HOME}/conda/envs
ENV DEQUINDRE_DIR ${HOME}/dequindre-demo
RUN mkdir -p ${DEQUINDRE_DIR}

# ----------------------------------------------------------------------------
# Build conda environments
# ----------------------------------------------------------------------------
# The conda envs don't change often. If we do the work here, we don't have to 
# recreate the conda environments on every build. 
# ----------------------------------------------------------------------------
COPY ./packages ${DEQUINDRE_DIR}/packages
COPY ./conda-envs ${DEQUINDRE_DIR}/conda-envs
RUN find ${DEQUINDRE_DIR} -name *.sh | xargs chmod +x
RUN find ${DEQUINDRE_DIR} -name *.sh | xargs dos2unix

# create every environment
RUN . ${DEQUINDRE_DIR}/conda-envs/setup-conda-envs.sh

# ----------------------------------------------------------------------------
# Setup image directory
# ----------------------------------------------------------------------------

COPY ./schedules ${DEQUINDRE_DIR}/schedules
COPY ./tasks/ ${DEQUINDRE_DIR}/tasks

# fix windows line endings 
RUN find ${DEQUINDRE_DIR} -name *.py | xargs chmod +x
RUN find ${DEQUINDRE_DIR} -name *.py | xargs dos2unix

ENTRYPOINT [ "python", "opt/dequindre-demo/schedules/demo.py" ]
