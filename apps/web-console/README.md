# web-console

## 概要

`web-console` は、AI駆動型広告文生成サービスのためのフロントエンドアプリケーションです。Vite + React をフレームワークとして採用し、shadcn/ui を使用して構築されています。ユーザーは直感的なインターフェースを通じて広告文の入力、生成リクエスト、および生成結果の確認を行うことができます。

## 技術スタック

* **フレームワーク**: Vite + React
* **UIフレームワーク**: shadcn/ui
* **スタイル**: Tailwind CSS
* **パッケージ管理**: npm
* **言語**: TypeScript

## 環境設定

`web-console` はバックエンド (`api-ad-generator`) と連携します。バックエンドのURLを環境変数として設定する必要があります。

* `NEXT_PUBLIC_API_BASE_URL`: バックエンドAPIのベースURL (例: `http://localhost:8000`)

## アーキテクチャ

本アプリケーションは、Vite + Reactの機能を最大限に活用し、コンポーネント指向のアプローチで構築されています。主要な関心事を分離し、保守性と拡張性を高めることを目指します。

### ディレクトリ構造

```
web-console/
├── src/                  # Reactアプリケーションのメインソース
│   ├── App.tsx           # メインアプリケーションコンポーネント
│   └── main.tsx          # アプリケーションのエントリーポイント
│
├── components/           # UIコンポーネント (再利用可能な部品)
│   ├── ui/               # shadcn/uiから生成されたコンポーネント
│   ├── common/           # アプリケーション共通のコンポーネント
│   └── specific/         # 特定のページや機能に特化したコンポーネント
│
├── lib/                  # ユーティリティ関数、ヘルパー、APIクライアントなど
│   ├── api.ts            # バックエンドAPIとの通信ロジック
│   ├── utils.ts          # 汎用ユーティリティ
│   └── hooks.ts          # カスタムReactフック
│
├── public/               # 静的アセット
├── styles/               # グローバルスタイル (Tailwind CSS設定など)
├── types/                # TypeScriptの型定義
├── .env.local.example
├── index.html            # Viteのエントリーポイント
├── vite.config.ts        # Vite設定ファイル
├── package.json
├── tsconfig.json
└── tailwind.config.ts
```

### 主要な責務

* **`src/`**: Reactアプリケーションのメインソースコードを配置します。App.tsxはメインアプリケーションコンポーネント、main.tsxはViteのエントリーポイントです。
* **`components/`**: UIの再利用性を高めるためのコンポーネント群を配置します。`shadcn/ui` を基盤としつつ、アプリケーション固有のコンポーネントも作成します。
* **`lib/`**: バックエンドAPIとの連携ロジック、データ整形、ユーティリティ関数など、純粋なビジネスロジックやヘルパー関数を配置し、コンポーネントから分離します。
* **`types/`**: アプリケーション全体で使用されるTypeScriptの型定義（APIのレスポンス型など）を一元管理します。

## パッケージ管理

* `npm` のみを使用
* 依存関係のインストール：`npm install`
* スクリプトの実行：`npm run [script_name]`
* パッケージの追加：`npm install [package_name]`
* パッケージの削除：`npm uninstall [package_name]`
* パッケージのアップグレード：`npm update [package_name]` (または `npm install [package_name]@latest` で特定パッケージの最新版へ)

## 開発環境のセットアップ

1.  **リポジトリのクローン:**
    ```bash
    git clone [リポジトリのURL]
    cd web-console
    ```
2.  **依存関係のインストール:**
    ```bash
    npm install
    ```
3.  **環境変数の設定:**
    `.env.local` ファイルを作成し、`NEXT_PUBLIC_API_BASE_URL` を設定してください。
    ```
    # .env.local の内容例
    NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
    ```
4.  **開発サーバーの起動:**
    ```bash
    npm run dev
    ```
    アプリケーションは `http://localhost:5173` で起動します（Viteのデフォルトポート）。

## コード品質

* **TypeScript**: すべてのコードに型ヒントを必須とする
* **Linting**: ESLint を使用し、コード規約を強制する
* **Prettier**: コードのフォーマットを統一する
* **コンポーネントの責務**: コンポーネントは集中して小さく保ち、単一責任の原則に従うこと
* **既存のパターン**: 既存のパターンを正確に踏襲すること

## テスト要件

* **テストフレームワーク**: Jest (単体テスト), React Testing Library (コンポーネントテスト), Playwright (E2Eテスト)
    * 単体テスト実行: `npm run test`
    * E2Eテスト実行: `npm run e2e` (または `npx playwright test`)
* **テストカバレッジ**: 主要な機能やUIコンポーネントはカバレッジを考慮してテストすること
* **新機能**: 新機能には必ずテストを追加すること
* **バグ修正**: バグ修正には関連するユニットテストまたはコンポーネントテストを追加すること
* **非同期テスト**: 非同期処理を含むテストは、適切な待機メカニズム（例: `await waitFor()`）を使用して安定性を確保すること
