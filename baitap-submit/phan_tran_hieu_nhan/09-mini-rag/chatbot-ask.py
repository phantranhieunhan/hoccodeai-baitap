import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from wikipediaapi import Wikipedia
import json
from typing import List, Optional


# ===== SETUP =====
client = OpenAI(base_url="http://localhost:1234/v1", api_key="random")

COLLECTION_NAME = "celebrity_bot"

db_client = chromadb.PersistentClient(path="./data")
db_client.heartbeat()

# By default, chromedb use `all-MiniLM-L6-v2` of Sentence Transformers
embedding_function = embedding_functions.DefaultEmbeddingFunction()

wiki = Wikipedia("HocCodeAI/0.0 (https://hoccodeai.com)", "en")

collection = db_client.get_or_create_collection(name=COLLECTION_NAME)

# ====== FUNCTION CALLING =====


def extract_entities_from_question(question: str) -> List[str]:
    """
    Extract potential celebrity/character names from user question using function calling
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_entities",
                "description": "Extract celebrity names, anime characters, or notable figures from a question",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entities": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of celebrity names, anime characters, or notable figures mentioned in the question",
                        }
                    },
                    "required": ["entities"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting celebrity names, anime characters, and notable figures from questions. Extract all relevant names that could be found on Wikipedia.",
            },
            {
                "role": "user",
                "content": f"Extract entities from this question: {question}",
            },
        ],
        tools=tools,
        tool_choice="required",  # force the OpenAI use function
    )
    if response.choices[0].message.tool_calls:
        function_args = json.loads(
            response.choices[0].message.tool_calls[0].function.arguments
        )
        return function_args.get("entities", [])
    return []


# from wikipedia api import Wikipedia
def get_wiki_content(entity_name: str) -> Optional[str]:
    """
    Retrieve Wikipedia content for a given entity
    """

    try:
        page = wiki.page(entity_name)
        if page.exists():
            return page.text
        else:
            # Try alternative formats
            alternatives = [
                entity_name.replace(" ", "_"),
                entity_name.replace("_", " "),
                entity_name.title(),
            ]

            for alt in alternatives:
                alt_page = wiki.page(alt)
                if alt_page.exists():
                    return alt_page.text
    except Exception as e:
        print(f"Error retrieving Wikipedia page for {entity_name}: {e}")
    return None


def add_entity_to_collection(entity_name: str) -> bool:
    """
    Add Wikipedia content for an entity to the collection
    """

    content = get_wiki_content(entity_name)
    if not content:
        return False

    # TODO: research more about this text chunk to getting more efficient
    chunks = content.split("\n\n")

    for i, chunk in enumerate(chunks):
        doc_id = f"{entity_name}_{i}"
        collection.add(
            documents=[chunk],
            ids=[doc_id],
            metadatas=[{"entity": entity_name, "chunk_index": i}],
        )
    return True


def query_collection(question: str, n_results: int = 3) -> List[str]:
    """
    Query the collection for relevant information
    """
    try:
        results = collection.query(query_texts=[question], n_results=n_results)
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        print(f"Error querying collection: {e}")
        return []


# response = client.chat.completions.create(
#     model="openai/gpt-oss-20b",
#     messages=messages,
#     tools=tools,
#     # Để temparature=0 để kết quả ổn định sau nhiều lần chạy
#     temperature=0,
# )


# # Đặt câu hỏi thông thường không dùng RAG
# response = client.chat.completions.create(
#     model="openai/gpt-oss-20b",
#     messages=[
#         {"role": "user", "content": prompt},
#     ],
# )

# print(response.choices[0].message.content)


def answer_question(question: str) -> str:
    """
    Main method
    """

    entities = extract_entities_from_question(question)

    if not entities:
        return "I couldn't identity any specific celebrity or character in your question. Could your please be more specific?"

    for entity in entities:
        success = add_entity_to_collection(entity)
        if not success:
            print(f"Could not find Wikipedia page for: {entity}")

    relevant_docs = query_collection(question, n_results=5)
    if not relevant_docs:
        return f"I couldn't find relevant information about {', '.join(entities)}. Please check if the names are spelled correctly."

    CONTEXT = "\n\n".join(relevant_docs)
    prompt = f"""
Use the following CONTEXT to answer the QUESTION at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer. Use an unbiased and journalistic tone.

CONTEXT: {CONTEXT}

QUESTION: {question}
"""

    print(prompt)

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions about celebrities and anime character based on provided context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI generation: {e}")


questions = [
    "Top hit songs of Sơn Tùng M-TP?",
]
for question in questions:
    print(f"\nQuestion: {question}")
    answer = answer_question(question)
    print(f"Answer: {answer}")
    print("-" * 50)
