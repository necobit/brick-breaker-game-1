# ブロック崩しゲーム (Brick Breaker Game)

## 説明

このプロジェクトは、QWEN3 の Cline による制御のテストとして作成されたブロック崩しゲームです。シンプルな操作で楽しめるアーケードスタイルのゲームです。

## 開発者

- プロジェクト名: Brick Breaker Game
- 開発者: Cline (QWEN3)
- リポジトリ: [necobit/brick-breaker-game-1](https://github.com/necobit/brick-breaker-game-1)

## Issue解決へのAI活用について

本プロジェクトのIssue対応・機能改善・デザイン調整等の一部は、
Windsurf + GPT-4.1 のAIアシスト機能を活用して行われています。
AIによる提案・自動化・コーディング支援により、より迅速かつ高品質な開発が実現されています。

## ゲーム操作方法

- **左右矢印キー**: パドルの移動
- **スペースバー**: ゲームの再開/一時停止 (初期状態では自動スタート)
- **マウスクリック**: ゲームの再開 (オプション操作)

## プロジェクト構造

```
brick-breaker-game-1/
├── tetris_env/          # ゲーム本体のロジック
│   └── brick_breaker.py
├── README.md            # このファイル
└── (他のリソースファイル)
```

## 起動方法

1. プロジェクトをクローンします:
   ```bash
   git clone https://github.com/necobit/brick-breaker-game-1.git
   ```
2. ゲームファイルを実行します:
   ```bash
   python tetris_env/brick_breaker.py
   ```

## テスト環境

- Python 3.10+
- ゲームエンジン: Pygame (必要に応じてインストール)
