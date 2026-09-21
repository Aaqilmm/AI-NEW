# LangChain Student Agent

A simple LangChain agent using Gemini, SQLite, and four tools.

## Tools

1. `get_student_info(student_id)`
2. `get_student_marks(student_id)`
3. `calculator(expression)`
4. `get_passing_rules()`

The agent chooses the required tools dynamically based on the question.

## Setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and add your Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Run:

```bash
python main.py
```

The `students.db` database is created automatically.

## Test Questions

```text
What is the name and department of student 22CS045?
```

```text
What are the marks of 22CS047?
```

```text
What is the total and average mark of 22CS045?
```

```text
Is 22CS045 eligible to pass according to the university rules?
```

Challenge:

```text
I am 22CS045. Tell me my name, department, total marks, average marks, and whether I satisfy the university passing requirements.
```
