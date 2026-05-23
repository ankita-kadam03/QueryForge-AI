# 🔥 QueryForge-AI

> **Fine-tuned Mistral 7B v0.3 for Natural Language → SQL Generation**
> Built with Unsloth + QLoRA on the SQLCoder dataset. 2x faster training, 70% less VRAM.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/QueryForge-AI/blob/main/QueryForge_AI_Finetune.ipynb)
[![HuggingFace Model](https://img.shields.io/badge/🤗%20HuggingFace-Model-yellow)](https://huggingface.co/YOUR_USERNAME/QueryForge-Mistral-7B-SQL)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

---

## 🎯 What is QueryForge-AI?

QueryForge-AI fine-tunes **Mistral 7B v0.3** to translate plain English into accurate SQL queries — schema-aware, production-ready, and blazing fast.

```
User  → "Show me the top 5 customers by revenue this month"
Model → SELECT customer_name, SUM(amount) AS total_revenue
        FROM orders
        WHERE MONTH(order_date) = MONTH(CURRENT_DATE)
        GROUP BY customer_name
        ORDER BY total_revenue DESC
        LIMIT 5;
```

**Real-world use cases:**
- 📊 Business analytics dashboards
- 🏢 Internal BI tools for non-technical teams
- 🤖 AI-powered database assistants
- 🔍 Data exploration platforms

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🧠 Base Model | Mistral 7B v0.3 |
| ⚡ Framework | Unsloth + QLoRA (2x faster, 70% less VRAM) |
| 📦 Dataset | `b-mc2/sql-create-context` (78,577 SQL pairs) |
| 🎯 Task | Natural Language → SQL (Text2SQL) |
| 🗄️ Schema-aware | Yes — uses CREATE TABLE context |
| 💾 Export formats | LoRA adapter, 16-bit merged, GGUF (Ollama) |
| 🖥️ GPU requirement | Free T4 (16GB) on Google Colab |

---

## 🚀 Quick Start

### Option 1: Run on Google Colab (Free GPU)
Click the badge above → Runtime → Run All → Done!

### Option 2: Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/QueryForge-AI.git
cd QueryForge-AI

# Install dependencies
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes
pip install datasets transformers

# Run training
jupyter notebook QueryForge_AI_Finetune.ipynb
```

### Option 3: Use the Pre-trained Model (HuggingFace)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model     = AutoModelForCausalLM.from_pretrained("YOUR_USERNAME/QueryForge-Mistral-7B-SQL")
tokenizer = AutoTokenizer.from_pretrained("YOUR_USERNAME/QueryForge-Mistral-7B-SQL")
```

### Option 4: Ollama (Local Inference)

```bash
ollama import queryforge-gguf/model.gguf
ollama run queryforge-sql
```

---

## 📊 Dataset

**`b-mc2/sql-create-context`** — 78,577 training examples

Each example has 3 fields:

| Field | Description | Example |
|---|---|---|
| `question` | Natural language question | "How many employees are in HR?" |
| `context` | CREATE TABLE schema | `CREATE TABLE employees (...)` |
| `answer` | Correct SQL query | `SELECT COUNT(*) FROM employees WHERE dept='HR'` |

### Prompt Template (Alpaca Format)

```
Below is an instruction that describes a SQL task, paired with context
that provides database schema information. Write a SQL query that
correctly answers the request.

### Instruction:
{question}

### Context (Database Schema):
{create_table_statements}

### SQL Query:
{answer}
```

---

## 🏋️ Training Configuration

```python
# Model
model_name    = "unsloth/mistral-7b-v0.3-bnb-4bit"
max_seq_length = 2048
load_in_4bit  = True

# QLoRA
r             = 16
lora_alpha    = 16
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                  "gate_proj", "up_proj", "down_proj"]

# Training
batch_size    = 2
grad_accum    = 4   # Effective batch = 8
epochs        = 1
learning_rate = 2e-4
optimizer     = "adamw_8bit"
```

---

## 🧪 Example Outputs

### E-commerce Revenue Query
```sql
-- Input: "Show top 5 customers by total spending this month"
SELECT c.customer_name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE MONTH(o.order_date) = MONTH(CURRENT_DATE)
  AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 5;
```

### HR Department Filter
```sql
-- Input: "List Engineering employees with salary above 80000"
SELECT e.emp_name, e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Engineering'
  AND e.salary > 80000;
```

### Aggregation & Analytics
```sql
-- Input: "Total revenue per product category for Q3 2024"
SELECT p.category, SUM(p.price * s.quantity) AS total_revenue
FROM products p
JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_date BETWEEN '2024-07-01' AND '2024-09-30'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

---

## 📁 Project Structure

```
QueryForge-AI/
│
├── QueryForge_AI_Finetune.ipynb  # Main training notebook
├── README.md
├── requirements.txt
├── LICENSE
│
├── app/                          # (Coming Soon) Web application
│   ├── backend/                  # FastAPI server
│   │   ├── main.py
│   │   └── inference.py
│   └── frontend/                 # React dashboard
│       └── src/
│
└── examples/
    ├── inference_demo.py         # Quick inference script
    └── sample_queries.md         # Example NL → SQL pairs
```

---

## 🗺️ Roadmap

- [x] Fine-tune Mistral 7B on SQL dataset
- [x] Schema-aware prompting (Alpaca format)
- [x] GGUF export for local inference
- [x] HuggingFace Hub upload
- [ ] FastAPI backend for inference
- [ ] React frontend with schema editor
- [ ] Live SQL execution + results table
- [ ] Docker deployment
- [ ] Query explanation feature
- [ ] SQL optimization suggestions

---

## ⚙️ Requirements

```
torch>=2.0
transformers>=4.40
unsloth
trl<0.9.0
peft
accelerate
bitsandbytes
datasets
```

Or just: `pip install -r requirements.txt`

---

## 🤝 Contributing

Pull requests welcome! Areas to contribute:
- More SQL benchmark evaluations
- Frontend web app
- Support for more SQL dialects (PostgreSQL, MySQL, SQLite)
- Dataset augmentation

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [Unsloth](https://github.com/unslothai/unsloth) — for the blazing fast fine-tuning framework
- [b-mc2/sql-create-context](https://huggingface.co/datasets/b-mc2/sql-create-context) — for the SQL dataset
- [Mistral AI](https://mistral.ai) — for the base model
- [defog.ai / SQLCoder](https://github.com/defog-ai/sqlcoder) — for SQL fine-tuning inspiration

---

<p align="center">
  Built with ❤️ | Fine-tuned on SQL | Powered by Unsloth + Mistral
</p>
