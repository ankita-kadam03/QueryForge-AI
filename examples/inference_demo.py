"""
QueryForge-AI — Inference Demo
================================
Run the fine-tuned model locally to generate SQL from natural language.

Usage:
    python examples/inference_demo.py

Requirements:
    pip install -r requirements.txt
"""

from unsloth import FastLanguageModel
import torch

# ── CONFIG ────────────────────────────────────────────────────────────────
MODEL_PATH     = "queryforge-lora-adapter"   # or "YOUR_USERNAME/QueryForge-Mistral-7B-SQL"
MAX_SEQ_LENGTH = 2048
# ──────────────────────────────────────────────────────────────────────────

ALPACA_SQL_PROMPT = """Below is an instruction that describes a SQL task, paired with context that provides database schema information. Write a SQL query that correctly answers the request.

### Instruction:
{instruction}

### Context (Database Schema):
{context}

### SQL Query:
{response}"""


def load_model(model_path: str):
    """Load the fine-tuned QueryForge model."""
    print(f"Loading model from: {model_path}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name     = model_path,
        max_seq_length = MAX_SEQ_LENGTH,
        dtype          = None,
        load_in_4bit   = True,
    )
    FastLanguageModel.for_inference(model)
    print("✅ Model loaded!")
    return model, tokenizer


def generate_sql(model, tokenizer, question: str, schema: str,
                 max_new_tokens: int = 256, temperature: float = 0.1) -> str:
    """
    Generate SQL from a natural language question + database schema.

    Args:
        model        : Fine-tuned model
        tokenizer    : Tokenizer
        question     : Natural language question
        schema       : CREATE TABLE statements (database schema)
        max_new_tokens: Max tokens to generate
        temperature  : Sampling temperature (lower = more deterministic)

    Returns:
        Generated SQL query string
    """
    prompt = ALPACA_SQL_PROMPT.format(
        instruction = question,
        context     = schema,
        response    = "",
    )

    inputs  = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens = max_new_tokens,
        use_cache      = True,
        temperature    = temperature,
        do_sample      = True,
    )

    generated = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens = True,
    )
    return generated.strip()


# ── Demo Examples ─────────────────────────────────────────────────────────
DEMO_EXAMPLES = [
    {
        "question": "Show the top 5 customers by total revenue this month",
        "schema": """
CREATE TABLE customers (
    customer_id   INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email         VARCHAR(100)
);
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,
    amount      DECIMAL(10,2),
    order_date  DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);"""
    },
    {
        "question": "How many employees work in each department?",
        "schema": """
CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(50)
);
CREATE TABLE employees (
    emp_id   INT PRIMARY KEY,
    emp_name VARCHAR(100),
    dept_id  INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);"""
    },
    {
        "question": "Find all products with stock below 10 units",
        "schema": """
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100),
    category     VARCHAR(50),
    price        DECIMAL(10,2),
    stock        INT
);"""
    },
]


if __name__ == "__main__":
    if not torch.cuda.is_available():
        print("⚠️  No GPU detected. Inference will be slow on CPU.")

    model, tokenizer = load_model(MODEL_PATH)

    print("\n" + "="*60)
    print("  QueryForge-AI — SQL Generation Demo")
    print("="*60)

    for i, example in enumerate(DEMO_EXAMPLES, 1):
        print(f"\n[Example {i}]")
        print(f"Question : {example['question']}")
        sql = generate_sql(model, tokenizer, example["question"], example["schema"])
        print(f"SQL      :\n{sql}")
        print("-"*60)

    # Interactive mode
    print("\n\n💬 Interactive Mode (type 'quit' to exit)")
    print("Enter your question and schema to generate SQL.\n")

    while True:
        question = input("Question: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            break

        print("Schema (paste CREATE TABLE statements, then press Enter twice):")
        schema_lines = []
        while True:
            line = input()
            if line == "":
                break
            schema_lines.append(line)
        schema = "\n".join(schema_lines)

        sql = generate_sql(model, tokenizer, question, schema)
        print(f"\n🔷 Generated SQL:\n{sql}\n")
        print("-"*60)
