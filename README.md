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
- Python 3.9 以上
- Ollama（ローカル LLM 実行環境）

---

## 1. リポジトリのクローン

```bash
git clone https://github.com/k-uryu224/paper_analyzer.git
cd paper_analyzer
