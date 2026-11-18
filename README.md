<table>
<tr>
<td width="100%" valign="middle">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=1000&size=40&pause=1000&color=0E75B6&center=true&vCenter=true&width=1000&lines=Pawan+Kumar+Sani;AI+Engineer;RAG+Systems+%7C+Agentic+Workflows+%7C+LLM+Serving" alt="Typing SVG" />

<p>
  <em>Building retrieval-augmented and agentic AI systems with LangChain &amp; LangGraph</em>
</p>

<p>
  <a href="https://linkedin.com/in/pawan-sani-224a2242b">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://x.com/PawanSani11">
    <img src="https://img.shields.io/badge/X-000000?style=flat-square&logo=x&logoColor=white" alt="X" />
  </a>
  <a href="mailto:pawan.sani321@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <br>
  <img src="https://img.shields.io/github/followers/PawanKumarSani?label=Followers&style=flat-square" alt="GitHub followers" />
  <img src="https://komarev.com/ghpvc/?username=PawanKumarSani&label=Profile+Views&color=0e75b6&style=flat-square" alt="Profile views" />
</p>

</td>
<td width="30%" align="center">
  <img src="https://i.gifer.com/Paz.gif" width="200" alt="Fun GIF" />
</td>
</tr>
</table>

<br>

## About

I design and build end-to-end AI systems — retrieval-augmented generation pipelines, multi-agent orchestration, and model serving — with a focus on making them production-ready rather than proof-of-concept.

- 🔭 Currently building RAG pipelines and multi-agent workflows with LangChain and LangGraph
- 🌱 Exploring LangGraph multi-agent patterns, model quantization, and inference optimization
- 🧠 Comfortable across the retrieval stack: chunking strategies, embedding models, vector databases (FAISS, ChromaDB), and citation-grounded generation
- 💬 Open to conversations on Python, RAG, LangChain, LangGraph, PyTorch, or AI agents
- 📫 **pawan.sani321@gmail.com**
- 🔗 **https://pawansani.lovable.app/**

<br>

## Tech Stack

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
<img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" />
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" />
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" />

<br>

<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square" />
<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square" />
<img src="https://img.shields.io/badge/FAISS-005571?style=flat-square" />
<img src="https://img.shields.io/badge/ChromaDB-6A4EFC?style=flat-square" />
<img src="https://img.shields.io/badge/Groq-F55036?style=flat-square" />
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />

<br>

<img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" />
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white" />

</div>

<br>

## Featured Projects

<table>
<tr>
<td width="33%" valign="top">

<h3>🤖 Multi-Agent Research Assistant</h3>

A LangGraph system where a deterministic supervisor routes between four specialized agents — <b>researcher, analyst, writer, and reviewer</b> — to research a topic end-to-end and produce a report.

The writer/reviewer pair loops until the draft is approved or a revision cap is hit, with real tool integrations (web, arXiv, Wikipedia) and checkpointed state for pause/resume.

<code>LangGraph</code> <code>Multi-Agent</code> <code>arXiv API</code> <code>Checkpointing</code>

<a href="https://github.com/Pawankumarsani/multi_agent_research_assistant"><img src="https://img.shields.io/badge/View%20Repository-%E2%86%92-0EA5E9?style=for-the-badge&logo=github&logoColor=white" alt="View Repository" /></a>

</td>
<td width="33%" valign="top">

<h3>🖼️ Multimodal RAG Pipeline</h3>

A RAG pipeline that processes PDFs containing both text and images, using <b>CLIP embeddings</b> for cross-modal retrieval, <b>FAISS</b> for vector search, and a <b>Groq-hosted LLM</b> for generation.

Structured as a clean, flat pipeline: <code>load_data → chunking → vectordb → retrieval → pipeline</code>.

<code>CLIP</code> <code>FAISS</code> <code>Groq</code> <code>Multimodal</code>

<a href="https://github.com/Pawankumarsani/multi_model_rag"><img src="https://img.shields.io/badge/View%20Repository-%E2%86%92-0EA5E9?style=for-the-badge&logo=github&logoColor=white" alt="View Repository" /></a>

</td>
<td width="33%" valign="top">

<h3>🧭 Agentic RAG</h3>

An agent-driven RAG system that decides <b>whether retrieval is needed</b>, retrieves from LangGraph/LangChain docs via FAISS, checks retrieved documents for relevance, rewrites the query when they fall short, and generates a grounded answer through a Streamlit chat interface.

<code>Self-Correction</code> <code>Query Rewriting</code> <code>FAISS</code> <code>Streamlit</code>

<a href="https://github.com/Pawankumarsani/Agentic_RAG"><img src="https://img.shields.io/badge/View%20Repository-%E2%86%92-0EA5E9?style=for-the-badge&logo=github&logoColor=white" alt="View Repository" /></a>

</td>
</tr>
</table>

---

## GitHub Stats

<div align="center">

<img src="https://streak-stats.demolab.com?user=Pawankumarsani&theme=tokyonight&hide_border=true&date_format=j%20M%5B%20Y%5D" alt="GitHub streak" />

<br/><br/>

<img src="https://img.shields.io/github/followers/Pawankumarsani?label=Followers&style=for-the-badge&color=0EA5E9&labelColor=0B1120" alt="GitHub followers" />
<img src="https://img.shields.io/badge/Focus-RAG%20%7C%20Agents%20%7C%20LLM%20Serving-1E3A8A?style=for-the-badge" alt="Focus" />
<img src="https://img.shields.io/badge/Status-Open%20to%20collaborate-22C55E?style=for-the-badge" alt="Status" />

</div>


---

## Contribution Activity

<div align="center">

</div>

<br/>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Pawankumarsani/Pawankumarsani/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Pawankumarsani/Pawankumarsani/output/github-snake.svg" />
  <img alt="Contribution snake eating my commit graph" src="https://raw.githubusercontent.com/Pawankumarsani/Pawankumarsani/output/github-snake.svg" width="100%" />
</picture>

<sub>Snake auto-generates every 12 hours from the workflow in <code>.github/workflows/snake.yml</code> — see the setup note below.</sub>

</div>

<br/>

<div align="center">

<img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Pawankumarsani&theme=tokyonight" width="100%" alt="Profile details summary" />

<table>
<tr>
<td><img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=Pawankumarsani&theme=tokyonight" alt="Repos per language" /></td>
<td><img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Pawankumarsani&theme=tokyonight" alt="Most commit language" /></td>
<td><img src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=Pawankumarsani&theme=tokyonight&utcOffset=5.5" alt="Productive time" /></td>
</tr>
</table>

</div>

<details>
<summary><b>⚙️ Snake setup (one-time, 2 minutes)</b></summary>

<br/>

The snake animation needs one workflow file in the profile repo — it does not render until that file exists and has run once.

1. In <code>Pawankumarsani/Pawankumarsani</code>, add <code>.github/workflows/snake.yml</code> (use the <code>snake.yml</code> provided alongside this README).
2. Commit to <code>main</code>, then open the <b>Actions</b> tab → <b>Generate Snake</b> → <b>Run workflow</b>.
3. Wait for the green tick — it pushes the SVGs to a new <code>output</code> branch.
4. Reload the profile. The snake appears in both light and dark mode.

No workflow, no snake — everything else on this page works immediately.

</details>

---

<div align="center">

### Let's build something that ships

<a href="mailto:pawan.sani321@gmail.com"><img src="https://img.shields.io/badge/Say%20Hello-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Say hello" /></a>
<a href="https://pawansani.lovable.app/"><img src="https://img.shields.io/badge/See%20My%20Work-0EA5E9?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio" /></a>

<br/><br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0EA5E9,50:1E3A8A,100:0B1120&height=120&section=footer" width="100%" />

</div>
