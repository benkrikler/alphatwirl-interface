FROM continuumio/miniconda:py27_latest

ENV PATH /opt/anaconda/bin:$PATH

RUN conda update conda --yes --quiet \
 && conda install --yes --quiet \
    flake8 \
    git \
    make \
    numpy \
    pip \
    pytest \
    setuptools \
 && conda clean -t -y

WORKDIR /code

CMD bash -c "source /code/ci/setup.sh" && bash -c "source /code/ci/test.sh"
