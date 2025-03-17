FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# OpenManusのクローン
RUN git clone https://github.com/mannaandpoem/OpenManus.git && \
    cd OpenManus && \
    uv pip install --system -r requirements.txt

# アプリケーションの依存関係のインストール
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

WORKDIR /app/OpenManus

# アプリケーションのコピー
COPY . .

# 必要なディレクトリの作成
RUN mkdir -p logs

# アプリケーションの起動
CMD ["python", "bot.py"]
