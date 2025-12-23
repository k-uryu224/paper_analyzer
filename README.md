# paper_analyzer

arXiv 上の論文を検索し、Abstract をもとに **日本語の構造化要約** を生成し、  
さらに生成されたレポート（Markdown）を使って **対話的に相談** できる研究支援ツールです。
ローカルで動作する LLM（Ollama）を利用します。

---

## 機能概要

- arXiv API を用いた論文検索
- Abstract をもとにした日本語構造化要約
  - 背景 / 目的 / 手法 / 結果 / 限界・課題
- 要約結果を `result.md` に保存
- `result.md` を根拠にした対話型相談モード

---

## 必要要件

- macOS / Linux（Windows でも可）
- Ollama（ローカル LLM 実行環境）

---
## セットアップ手順

1. リポジトリ

```bash
git clone https://github.com/k-uryu224/paper_analyzer.git
cd paper_analyzer

---

2. Python仮想環境の作成

python3 -m venv .venv

---

3. 仮想環境の有効化

macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\Activate.ps1

---

4.依存ライブラリのインストール

pip install requests

---

5.Ollama のセットアップ

# Ollama が未インストールの場合は以下から取得

https://ollama.com/

# 使用するモデルを取得

ollama pull qwen2.5:7b

# モデル一覧を確認

ollama list

---

プログラムの実行

python main.py

---

7.実行時の入力例

> 検索クエリ: transformer robustness
> 論文数: 3

---

8.実行フロー

arXiv API で論文を検索
Abstract を取得
Ollama で日本語の構造化要約を生成
result.md に保存
対話モード（任意）へ移行

---

9.相談モードの使い方

result.md を使って相談しますか？ (y/n):
質問: これらの論文に共通する課題は何ですか？
・回答は result.md の内容のみ を根拠に生成されます
・関連する論文番号・タイトルが明示されます
・Enter のみで終了します

