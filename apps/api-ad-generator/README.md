# api-ad-generator

## 概要

`api-ad-generator` は、AI（Claude）を活用して広告文を生成するためのバックエンドサービスです。本サービスは、ドメイン駆動設計とクリーンアーキテクチャの原則に従って構築されており、FastAPI をフレームワークとして使用しています。データベースは使用せず、広告文生成のロジックに特化しています。

## 技術スタック

* **フレームワーク**: FastAPI
* **LLM**: Claude (Anthropic API)
* **パッケージ管理**: uv
* **言語**: Python

## 環境設定

`api-ad-generator` を実行する前に、以下の環境変数を設定してください。

* `ANTHROPIC_API_KEY`: Anthropic API にアクセスするためのAPIキー。

## 設計原則

本プロジェクトは、**ドメイン駆動設計 (DDD)** と **クリーンアーキテクチャ** の原則に従って設計されています。これにより、ビジネスロジックと技術的詳細が分離され、テスト容易性、保守性、およびスケーラビリティが向上します。

### アーキテクチャのレイヤー構造

プロジェクトのディレクトリ構造は、クリーンアーキテクチャの原則に基づいています。

```
api-ad-generator/
├── app/
│   ├── domain/               # ドメイン層: ビジネスロジックの中核 (Entities, Value Objects, Domain Services, Repositories Interfaces)
│   │   ├── entities/         # ドメインオブジェクト（例: AdCopy, AdInput）
│   │   ├── services/         # ドメインサービス（例: AdGenerationDomainService）
│   │   └── repositories/     # リポジトリインターフェース（ここではDBがないため、主に外部APIの抽象化インターフェース）
│   │
│   ├── application/          # アプリケーション層: ユースケースの定義と調整 (Use Cases, Application Services)
│   │   ├── usecases/         # ユースケース（例: GenerateAdCopyUseCase）
│   │   └── services/         # アプリケーションサービス
│   │
│   ├── infrastructure/       # インフラストラクチャ層: 外部とのやり取り (Adapters, External Services, Framework details)
│   │   ├── api/              # FastAPIのルーター定義、リクエスト/レスポンスモデル
│   │   ├── clients/          # 外部APIクライアント（例: Claude APIクライアント）
│   │   └── config/           # 環境変数設定など
│   │
│   ├── main.py               # FastAPIアプリケーションのエントリポイント
│   └── dependencies.py       # 依存性注入の設定
│
├── tests/                    # テストコード
├── .env.example
├── requirements.txt
└── pyproject.toml / uv.lock  # uvによるロックファイル
```

### 各レイヤーの役割

#### 1. ドメイン層 (`app/domain/`)

この層はアプリケーションの**核**であり、**ビジネスロジックとルール**のみを含みます。外部のフレームワークや永続化のメカニズムには依存しません。

* **Entities (エンティティ)**: 広告文の構造 (`AdCopy`), 入力データ (`AdInput`) など、ビジネスで識別可能なオブジェクト。ライフサイクルを持ち、IDで識別されます。
* **Value Objects (値オブジェクト)**: 意味的な概念を表現するオブジェクトで、IDを持たず、その属性によって識別されます（例: `Tone`, `AppealPoint`）。
* **Domain Services (ドメインサービス)**: 複数のエンティティや値オブジェクトにまたがるビジネスロジック、あるいは特定のエンティティに属さない重要なビジネスルール。
* **Repositories Interfaces (リポジトリインターフェース)**: 永続化（今回は外部API呼び出し）のための抽象的なインターフェース。**実装はインフラストラクチャ層に属します。**

#### 2. アプリケーション層 (`app/application/`)

ドメイン層を**オーケストレーション**し、ユーザーからのリクエストや外部イベントに対応する**ユースケース**を定義します。

* **Use Cases (ユースケース)**: 特定のユーザー操作やシステム機能の実行を定義します（例: `GenerateAdCopyUseCase`）。ドメイン層のサービスやリポジトリインターフェースを呼び出し、ビジネスフローを調整します。
* **Application Services (アプリケーションサービス)**: ユースケースの実行を管理し、トランザクションやセキュリティなど、アプリケーション全体の調整を行います。

#### 3. インフラストラクチャ層 (`app/infrastructure/`)

この層は、アプリケーションの**外部とのやり取り**を処理します。具体的な技術的詳細、フレームワーク依存性、永続化の実装、外部APIクライアントなどが含まれます。

* **API (FastAPI)**: HTTPリクエストを受け取り、アプリケーション層のユースケースを呼び出します。Pydanticモデルによるリクエスト/レスポンスのバリデーションもここで行います。
* **Clients (外部サービス)**: Claude API など、外部システムとの具体的な通信を行います。ドメイン層で定義されたリポジトリインターフェースの**実装**がここに含まれます。
* **Config (設定)**: 環境変数の読み込みなど、アプリケーションの設定を管理します。

### 依存性の方向性

クリーンアーキテクチャの原則として、**依存性は常に外側から内側へ**向かいます。

`インフラストラクチャ層` $\to$ `アプリケーション層` $\to$ `ドメイン層`

これにより、内側の層は外側の層の変更に影響されず、ビジネスロジックの安定性を保ちます。

## パッケージ管理

* `uv` のみを使用し、`pip` は絶対に使わない
* インストール方法：`uv add package`
* ツールの実行：`uv run tool`
* アップグレード：`uv add --dev package --upgrade-package package`
* 禁止事項：`uv pip install`、`@latest` 構文の使用

## 開発環境のセットアップ

1.  **リポジトリのクローン:**
    ```bash
    git clone [リポジトリのURL]
    cd api-ad-generator
    ```
2.  **uv のインストール:**
    ```bash
    # uv のインストール方法（公式ドキュメントを参照してください）
    # 例: curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
3.  **依存関係のインストール:**
    ```bash
    uv sync
    ```
4.  **環境変数の設定:**
    `ANTHROPIC_API_KEY` を適切に設定してください。
    ```bash
    export ANTHROPIC_API_KEY="your_anthropic_api_key"
    ```
    (開発時は `.env` ファイルを使用することも検討してください。ただし、本番環境ではセキュアな方法で管理してください。)

## サービス実行

開発サーバーを起動するには、以下のコマンドを実行します。

```bash
uv run uvicorn app.main:app --reload
```

APIドキュメントは、サービス起動後に `http://localhost:8000/docs` で確認できます。

## コード品質

* すべてのコードに**型ヒント**を必須とする
* パブリックAPIには必ず**ドキュメンテーション文字列（docstring）**を付ける
* 関数は集中して小さく保つこと
* 既存のパターンを正確に踏襲すること
* 行の最大長は88文字まで

## テスト要件

* テストフレームワーク：`uv run --frozen pytest`
* 非同期テストは `asyncio` ではなく `anyio` を使用
* カバレッジはエッジケースやエラーも含めてテストすること
* 新機能には必ずテストを追加すること
* バグ修正にはユニットテストを追加すること
