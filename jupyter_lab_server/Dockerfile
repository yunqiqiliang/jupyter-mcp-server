ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

    RUN pip install --upgrade pip && \
    pip install jupyterlab ipykernel \
        jupyter_collaboration==2.0.1 \
        datalayer_pycrdt \
        clickzetta-connector-python \
        clickzetta-zettapark-python \
        matplotlib plotly seaborn pandas numpy \
        scikit-learn statsmodels xgboost lightgbm catboost \
        tensorflow torch prophet sktime mlforecast


RUN jupyter server extension enable jupyter_collaboration --py --sys-prefix

WORKDIR /mcp_notebook

# 只设置非敏感环境变量，JUPYTER_TOKEN 建议运行时传递
ENV JUPYTER_PORT=8888
ENV JUPYTER_EXTRA_ARGS="--ip=0.0.0.0 --no-browser --allow-root"

# 用 shell 启动，支持环境变量注入
# CMD ["sh", "-c", "jupyter lab --port=${JUPYTER_PORT} --IdentityProvider.token=${JUPYTER_TOKEN} ${JUPYTER_EXTRA_ARGS}"]

# EXPOSE 8888