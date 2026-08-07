FROM debian:bookworm-slim

# libstdc++6 for numpy's C extensions; the biocontainer shipped none of its own.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        libstdc++6 \
    && rm -rf /var/lib/apt/lists/*


ARG PYTHON_URL=https://github.com/astral-sh/python-build-standalone/releases/download/20260728/cpython-3.10.20%2B20260728-x86_64-unknown-linux-gnu-install_only.tar.gz
ARG PYTHON_SHA256=5b6ae36e239727dd9b9c567023261e8b2fdd716d25dde2b15d68bf105b782856
RUN curl -fsSL -o /tmp/python.tar.gz "$PYTHON_URL" \
    && echo "$PYTHON_SHA256  /tmp/python.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/python.tar.gz -C /opt \
    && rm /tmp/python.tar.gz

# tarball unpacks to /opt/python; interface Dockerfiles resolve `command -v python`.
ENV PATH=/opt/python/bin:$PATH
RUN ln -s /opt/python/bin/python3 /usr/local/bin/python \
    && ln -s /opt/python/bin/pip3 /usr/local/bin/pip


COPY --from=quay.io/biocontainers/baysor:0.7.1--h467016e_2 /usr/local/bin/baysor /usr/local/bin/baysor
COPY --from=quay.io/biocontainers/baysor:0.7.1--h467016e_2 /usr/local/lib/baysor /usr/local/lib/baysor

RUN python --version && python -m pip --version && baysor --version

CMD ["/bin/bash"]
