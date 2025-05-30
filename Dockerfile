# Copyright (c) 2023-2024 Datalayer, Inc.
# Copyright (c) 2025 Alexander Isaev
# BSD 3-Clause License

# 使用构建参数指定基础镜像，默认为 python:3.10-slim
ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY LICENSE LICENSE
COPY README.md README.md
COPY jupyter_mcp_server/* jupyter_mcp_server/

# Install main package, dependencies, AND Pillow
RUN pip install -e . Pillow 

# Add "name" field to awareness state in jupyter_nbmodel_client to fix KeyError in jupyter_collaboration v2.0.1
RUN sed -i '/"owner": self._username,/a \                "name": self._username,' /usr/local/lib/python3.10/site-packages/jupyter_nbmodel_client/client.py \
    && echo "Patched jupyter_nbmodel_client/client.py to include user name in awareness." \
    || echo "WARNING: Failed to patch jupyter_nbmodel_client/client.py"

RUN pip uninstall -y pycrdt datalayer_pycrdt
RUN pip install datalayer_pycrdt

RUN apt-get update && apt-get install -y tini && apt-get clean

# tini 作为 init 进程，能正确捕获和转发信号，主进程退出后容器自动退出
# 无论与其它服务器是否仍有连接，只要主进程退出，容器即退出
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-m", "jupyter_mcp_server.server"]