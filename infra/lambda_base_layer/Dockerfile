FROM amazonlinux:2

# Install Python
RUN yum -y install gcc-c++ openssl-devel bzip2-devel libffi-devel wget tar gzip make sqlite-devel.x86_64 which xz graphviz graphviz-devel && \
    cd /opt && \
    wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz && \
    tar xzf Python-3.9.6.tgz && \
    ls && \
    cd Python-3.9.6 && \
    ls && \
    ./configure --enable-loadable-sqlite-extensions --enable-optimizations && \
    make altinstall && \
    rm -f /opt/Python-3.9.6.tgz && \
    cd /opt
    # wget https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/4.0.0/graphviz-4.0.0.tar.gz && \
    # tar -xvzf graphviz-4.0.0.tar.gz && \
    # cd graphviz-4.0.0 && \
    # ./configure && \
    # make && \
    # make install && \
    # rm -f /opt/graphviz-4.0.0.tar.xz && \
    # cd /opt

RUN export PATH=$PATH:~/usr/bin
RUN export PATH=$PATH:~/usr/bin/dot
RUN export PATH=$PATH:~/opt/bin
RUN export PATH=$PATH:~/opt/bin/dot
RUN dot -V && \
    which dot
RUN echo "$PATH"

# Install zip
RUN yum install -y zip

RUN yum clean all

# Set up PIP and Venv
RUN python3.9 -m pip install --upgrade pip && \
    python3.9 -m pip install virtualenv
RUN python3.9 -m venv base
RUN source base/bin/activate

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt -t ./python
RUN python3.9 -m pip install nltk
RUN python3.9 -m nltk.downloader stopwords

# Zip it up for deployment.
RUN zip -r layer.zip ./python/ /usr/bin /usr/lib64
ENTRYPOINT ["/bin/bash", "-l"]