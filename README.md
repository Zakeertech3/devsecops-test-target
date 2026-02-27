# Elastic MCP PR Reviewer

An autonomous GitHub agent that uses Elastic vector search and the GitHub Model Context Protocol (MCP) to semantically match new Pull Requests against historical vulnerabilities, injecting secure code fixes directly into the PR.

---

## The Problem Statement
Software engineering teams suffer from an "institutional memory" problem. Despite having thousands of past Pull Requests where senior engineers have already identified, debated, and fixed complex security flaws, that data is trapped in closed PRs. Traditional security scanners (SAST) rely on rigid regex rules and completely miss context-dependent logic flaws. As a result, developers repeat the exact same mistakes, and senior reviewers waste hours catching identical vulnerabilities.

## The Solution
We built an Agentic DevSecOps Auditor that turns dead PR history into an active security guard. By building an ETL pipeline to vectorize 5,000 historical PRs, we gave the AI a company-specific memory. It leverages an Elastic Cloud vector database to understand the *logic* of the code (bypassing regex limitations) and utilizes the **Model Context Protocol (MCP)** to autonomously read live GitHub code and write secure fixes directly to the developer's PR without human intervention.

---

## Architecture Flow

```text
================================= PHASE 1: THE VECTOR BRAIN (ETL) =================================

+-----------------------+    Extract    +------------------------+    Bulk Load   +-----------------------+
|     Data Sources      | =============>|    Local Python ETL    | ==============>|   Elastic Cloud DB    |
|-----------------------|               |------------------------|                |-----------------------|
| Hugging Face Dataset  |               | - Pandas / PyArrow     |                | Index:                |
| 'hao-li/AIDev'        |               | - SentenceTransformers |                | 'pr-code-reviews'     |
| (5k Historical PRs)   |               |   ('all-MiniLM-L6-v2') |                | (384D Vectors mapped  |
+-----------------------+               +------------------------+                |  for kNN search)      |
                                                                                  +-----------------------+
                                                                                             ^
                                                                                             |
================================= PHASE 2: THE DEVSECOPS AGENT LOOP =========================|=======
                                                                                             |
                                                                            [Tool: codebase.search_prs]
                                                                                             |
                                                                                  +-----------------------+
                                                                                  | Elastic Agent Builder |
+-----------------------+               +------------------------+                |-----------------------|
|   Target GitHub Repo  |               |    Local MCP Server    |                | Agent:                |
|-----------------------|               |------------------------|                | DevSecOps Auditor     |
| Zakeertech3/          |  Read/Write   | Node.js Environment    |  HTTP Stream   |                       |
| devsecops-test-target | <============ | Auth: GitHub PAT       | <=============>| MCP Tools Bridged:    |
|                       |  (GitHub API) |                        |  (Pinggy.io +  | - get_pull_request    |
| - Live PR Code Diffs  |               | Exposes Actions:       |  Supergateway) | - get_file_contents   |
| - Auto-Issue Comments |               | - get_pull_request     |                | - add_issue_comment   |
+-----------------------+               | - get_file_contents    |                +-----------------------+
                                        | - add_issue_comment    |                            ^
                                        +------------------------+                            |
                                                                                         Chat Prompt
                                                                                              |
                                                                                  +-----------------------+
                                                                                  |    Developer (You)    |
                                                                                  +-----------------------+




---
```

## Tech Stack
* **Cloud & Search:** Elastic Cloud, Elasticsearch Vector Database, Elastic Agent Builder
* **Data Engineering:** Python, Pandas, PyArrow, Parquet
* **Machine Learning:** Hugging Face (`hao-li/AIDev`), SentenceTransformers (`all-MiniLM-L6-v2`)
* **Agentic Framework:** Model Context Protocol (MCP), `@modelcontextprotocol/server-github`
* **Networking & Security:** Pinggy.io, Supergateway, Node.js, GitHub Fine-Grained PATs

## Future Scope (V2)
Currently, the agent is triggered manually via the Elastic chat interface. The next iteration will implement an **Event-Driven Architecture**. By deploying a lightweight Python webhook listener, GitHub `pull_request.opened` events will automatically trigger the Elastic Agent API, resulting in a 100% zero-touch, fully automated DevSecOps pipeline.
