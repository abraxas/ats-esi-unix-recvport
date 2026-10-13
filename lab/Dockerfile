# Shared Apache Traffic Server 10.2.0 lab image (ats-10.2.0-lab:local).
# Build context is the pinned trafficserver source tree. Do not embed host paths.
FROM ubuntu:24.04 AS build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        g++ \
        libbrotli-dev \
        libcap-dev \
        libfmt-dev \
        libhwloc-dev \
        libjemalloc-dev \
        libluajit-5.1-dev \
        liblzma-dev \
        libmagick++-dev \
        libpcre2-dev \
        libpcre3-dev \
        libssl-dev \
        libunwind-dev \
        libxml2-dev \
        libzstd-dev \
        ninja-build \
        pkg-config \
        python3 \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /src

RUN cmake -S /src -B /build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/ats \
        -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF \
        -DBUILD_TESTING=OFF \
        -DBUILD_REGRESSION_TESTING=OFF \
        -DENABLE_AUTEST=OFF \
        -DBUILD_EXPERIMENTAL_PLUGINS=ON \
        -DENABLE_QUICHE=OFF \
        -DENABLE_CRIPTS=ON \
        -DENABLE_EXAMPLE=OFF \
        -DENABLE_DOCS=OFF \
        -DENABLE_VERIFY_PLUGINS=OFF \
    && cmake --build /build --parallel 2 \
    && cmake --install /build \
    && /opt/ats/bin/traffic_server --version \
    && rm -rf /build /src

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/opt/ats/bin:/usr/local/trafficserver/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libbrotli1 \
        libcap2 \
        libfmt9 \
        libhwloc15 \
        libjemalloc2 \
        libluajit-5.1-2 \
        liblzma5 \
        libmagick++-6.q16-9t64 \
        libpcre2-8-0 \
        libpcre3 \
        libssl3t64 \
        libunwind8 \
        libxml2 \
        libzstd1 \
        zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/ats /opt/ats

RUN mkdir -p /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver \
    && chown -R nobody:nogroup /opt/ats/var \
    && chmod a+rX /opt/ats

EXPOSE 8080

CMD ["traffic_server"]
