import os
import sqlite3
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

DB_NAME = "students.db"


def create_database():
    """Create the students table and insert the assignment data."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            python INTEGER NOT NULL,
            database_mark INTEGER NOT NULL,
            ai INTEGER NOT NULL,
            web INTEGER NOT NULL
        )
    """)

    students = [
        ("22CS045", "Dhanushya", "Computer Science", 85, 72, 90, 78),
        ("22CS046", "Rahul", "Computer Science", 65, 70, 68, 72),
        ("22CS047", "Priya", "Information Technology", 92, 88, 95, 90),
        ("22CS048", "Arun", "Information Technology", 55, 60, 58, 62),
        ("22CS049", "Meena", "Computer Science", 78, 85, 80, 88),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO students
        (student_id, name, department, python, database_mark, ai, web)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, students)

    conn.commit()
    conn.close()


@tool
def get_student_info(student_id: str) -> str:
    """
    Get a student's name and department using their student ID.
    Use this tool when the user asks for a student's name or department.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, department
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return f"No student found with ID {student_id}."

    name, department = result
    return f"Name: {name}\nDepartment: {department}"


@tool
def get_student_marks(student_id: str) -> str:
    """
    Get a student's Python, Database, AI, and Web marks.
    Use this tool when the user asks about a student's marks.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT python, database_mark, ai, web
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return f"No student found with ID {student_id}."

    python_mark, database_mark, ai_mark, web_mark = result

    return (
        f"Python: {python_mark}\n"
        f"Database: {database_mark}\n"
        f"AI: {ai_mark}\n"
        f"Web: {web_mark}"
    )


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.
    Use this tool for total marks, average marks, and other arithmetic.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as error:
        return f"Calculation error: {error}"


@tool
def get_passing_rules() -> str:
    """
    Get the university passing rules.
    Minimum overall average is 40 percent and minimum mark in
    every subject is 35.
    """
    return (
        "Passing Rules:\n"
        "- Minimum overall average: 40%\n"
        "- Minimum mark in each subject: 35"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

tools = [
    get_student_info,
    get_student_marks,
    calculator,
    get_passing_rules,
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a student information assistant.

Use the available tools to answer student-related questions.
Do not guess student information or marks.

For total or average questions, retrieve the marks and use the
calculator tool.

For passing eligibility, retrieve the marks, retrieve the passing
rules, and use the calculator when arithmetic is required.

Choose tools dynamically based on the user's question.
Do not follow a fixed tool sequence.
Give a clear final answer.
"""
)


def ask_agent(question: str):
    """Send one question to the LangChain agent and print the answer."""
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    print("\nANSWER:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    create_database()

    print("students.db created successfully.")
    print("LangChain + Gemini student agent is ready.")

    while True:
        question = input("\nAsk a question (type 'exit' to stop): ")

        if question.lower().strip() == "exit":
            print("Goodbye!")
            break

        ask_agent(question)
