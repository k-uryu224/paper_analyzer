import os
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

# =========================
# 設定
# =========================

OLLAMA_MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

OUT_MD = "result.md"


# =========================
# arXiv 論文検索
# =========================

def fetch_arxiv_papers(query: str, max_results: int = 5) -> List[Dict]:
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{query.replace(' ', '+')}"
        f"&start=0&max_results={max_results}"
    )

    r = requests.get(url, timeout=15)
    r.raise_for_status()

    root = ET.fromstring(r.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for e in root.findall("atom:entry", ns):
        papers.append({
            "arxiv_id": e.find("atom:id", ns).text.split("/")[-1],
            "title": e.find("atom:title", ns).text.strip(),
            "abstract": e.find("atom:summary", ns).text.strip()
        })

    return papers


# =========================
# Ollama 呼び出し
# =========================

def ollama_generate(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["response"].strip()


# =========================
# 構造化要約（Abstractベース）
# =========================

def structured_summary(title: str, abstract: str) -> str:
    prompt = f"""
あなたは大学生向けの研究支援AIです。
以下の論文を **日本語で** 構造化要約してください。

【タイトル】
{title}

【Abstract】
{abstract}

以下の形式を必ず守ってください。

### {title}

**背景**
（2〜3文）

**目的**
（1〜2文）

**手法**
（2〜3文）

**結果**
（2〜3文）

**限界・課題**
（1〜2文）
"""
    return ollama_generate(prompt)


# =========================
# Markdown 保存
# =========================

def save_markdown(query: str, papers: List[Dict]):
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# 論文調査レポート\n\n")
        f.write(f"## 検索クエリ\n{query}\n\n")

        for i, p in enumerate(papers, 1):
            f.write(f"## 論文 {i}\n\n")
            f.write(structured_summary(p["title"], p["abstract"]))
            f.write("\n\n---\n\n")


# =========================
# Markdown 読み込み
# =========================

def load_markdown(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} が見つかりません")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# =========================
# result.md を使った相談モード
# =========================

def consult_with_markdown(markdown_text: str):
    print("\n論文調査結果をもとに相談できます")
    print("（Enterのみで終了）\n")

    while True:
        question = input("質問: ").strip()
        if question == "":
            print("対話を終了します")
            break

        prompt = f"""
あなたは研究指導を行う大学院レベルの研究アシスタントです。
以下は、事前に調査・要約された論文レポートです。

====================
{markdown_text}
====================

この内容を根拠として、次の質問に日本語で丁寧に答えてください。

質問:
{question}

制約:
- 上記レポートに基づいて回答すること
- 関連する場合は「どの論文（番号・タイトル）」かを明示すること
"""

        print("\n回答中...\n")
        answer = ollama_generate(prompt)
        print(answer)
        print("\n" + "-" * 60 + "\n")


# =========================
# メイン処理
# =========================

def main():
    query = input("> 検索クエリ: ")
    top_k = int(input("> 論文数: "))

    print("\narXiv 検索中...")
    papers = fetch_arxiv_papers(query, max_results=top_k)

    if len(papers) == 0:
        print("論文が見つかりませんでした")
        return

    print("要約生成中（Ollama）...")
    save_markdown(query, papers)

    print(f"\n完了: {OUT_MD} に保存しました")

    use_consult = input("\nresult.md を使って相談しますか？ (y/n): ")
    if use_consult.lower() == "y":
        md_text = load_markdown(OUT_MD)
        consult_with_markdown(md_text)


if __name__ == "__main__":
    main()
