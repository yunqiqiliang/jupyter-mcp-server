ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git build-essential \
    # 安装中文字体包
    fonts-wqy-microhei fonts-wqy-zenhei fonts-noto-cjk \
    # 增加更多中文字体选项
    fonts-arphic-ukai fonts-arphic-uming \
    fonts-arphic-gbsn00lp fonts-arphic-bkai00mp \
    fonts-noto-cjk-extra \
    # 安装中文黑体字体（替代SimHei）
    fonts-noto-cjk-extra fonts-hanazono \
    # 安装DejaVu Sans字体
    fonts-dejavu-core fonts-dejavu \
    # 安装Arial字体替代品
    fonts-liberation \
    # 安装工具
    fontconfig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 更新字体缓存并列出可用字体
RUN fc-cache -fv && \
    echo "==== 列出系统可用字体 ====" && \
    fc-list :lang=zh | sort

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        jupyterlab ipykernel \
        jupyter_collaboration==2.0.1 \
        datalayer_pycrdt \
        clickzetta-connector-python \
        clickzetta-zettapark-python \
        matplotlib plotly seaborn pandas numpy \
        statsmodels  scikit-learn prophet xgboost lightgbm \
        tabulate && \
    # 清理pip缓存
    rm -rf /root/.cache/pip && \
    # 清理Python的字节码文件
    find /usr/local -name __pycache__ -type d -exec rm -rf {} +

RUN jupyter server extension enable jupyter_collaboration --py --sys-prefix

WORKDIR /mcp_notebook

# 只设置非敏感环境变量，JUPYTER_TOKEN 建议运行时传递
ENV JUPYTER_PORT=8888
ENV JUPYTER_EXTRA_ARGS="--ip=0.0.0.0 --no-browser --allow-root"

# 删除以前的配置方式
RUN rm -rf /root/.ipython/profile_default/startup/* \
    /etc/ipython/startup/* \
    /etc/ipython/profile_default/startup/* \
    # 删除下载的包和缓存
    /tmp/* /var/tmp/*

# 创建用户级 matplotlib 配置目录 - 只用系统自带字体
RUN mkdir -p /root/.config/matplotlib && \
    echo "font.family: sans-serif" > /root/.config/matplotlib/matplotlibrc && \
    echo "font.sans-serif: WenQuanYi Micro Hei, Noto Sans CJK SC, WenQuanYi Zen Hei, DejaVu Sans" >> /root/.config/matplotlib/matplotlibrc && \
    echo "axes.unicode_minus: False" >> /root/.config/matplotlib/matplotlibrc && \
    echo "font.size: 12" >> /root/.config/matplotlib/matplotlibrc

# 创建启动脚本，只检测和使用已知存在的字体
RUN mkdir -p /etc/ipython/profile_default/startup && \
    echo "# 只用系统自带中文字体，彻底避免SimHei" > /etc/ipython/profile_default/startup/00-setup.py && \
    echo "print('配置matplotlib中文字体环境...')" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "try:" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    import os" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    import matplotlib" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    font_candidates = [" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'," >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'," >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'," >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    ]" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    font_path = None" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    for f in font_candidates:" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        if os.path.exists(f):" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "            font_path = f" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "            print(f'使用字体: {font_path}')" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "            break" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    if not font_path:" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        print('未找到中文字体，可能无法正常显示中文')" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    matplotlib.rcParams['font.family'] = 'sans-serif'" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'DejaVu Sans']" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    matplotlib.rcParams['axes.unicode_minus'] = False" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    from matplotlib import font_manager" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    def chinese_font():" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        if font_path: return font_manager.FontProperties(fname=font_path)" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "        else: return font_manager.FontProperties()" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    print('✅ 中文字体配置完成，可用chinese_font()用作fontproperties')" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "except Exception as e:" >> /etc/ipython/profile_default/startup/00-setup.py && \
    echo "    print('❌ 字体配置失败:', e)" >> /etc/ipython/profile_default/startup/00-setup.py

# 创建默认IPython配置 - 简化为只加载单一脚本
RUN mkdir -p /etc/ipython && \
    echo "c.InteractiveShellApp.exec_files = ['/etc/ipython/profile_default/startup/00-setup.py']" > /etc/ipython/ipython_config.py

# 创建自定义内核，确保预加载模块
RUN mkdir -p /usr/local/share/jupyter/kernels/python3-datascience/ && \
    echo '{' > /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '  "display_name": "Python 3 (Data Science)",' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '  "language": "python",' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '  "argv": [' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '    "python",' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '    "-c",' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '    "exec(open(\"/etc/ipython/profile_default/startup/00-setup.py\").read()); from ipykernel_launcher import main; main()",' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '    "-f",' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '    "{connection_file}"' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '  ]' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json && \
    echo '}' >> /usr/local/share/jupyter/kernels/python3-datascience/kernel.json

# 配置默认使用数据科学内核
RUN mkdir -p /etc/jupyter && \
    echo 'c.NotebookApp.kernel_spec_manager_class = "jupyter_client.kernelspec.KernelSpecManager"' > /etc/jupyter/jupyter_notebook_config.py && \
    echo 'c.LabServerApp.default_kernel_name = "python3-datascience"' >> /etc/jupyter/jupyter_notebook_config.py

# 最终清理 - 减少镜像大小
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    # 清理pip缓存
    rm -rf /root/.cache/pip && \
    # 清理文档
    rm -rf /usr/share/doc/* /usr/share/man/* && \
    # 清理Python缓存
    find /usr/local -name '*.pyc' -delete && \
    find /usr/local -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true && \
    # 清理不必要的locale文件
    rm -rf /usr/share/locale/* && \
    # 压缩日志文件
    find /var/log -type f -exec truncate --size=0 {} \;