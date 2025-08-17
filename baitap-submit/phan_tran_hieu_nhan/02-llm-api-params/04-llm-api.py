from openai import OpenAI
import textwrap

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="random"
)  

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def split_into_chunks(text: str, max_chars=3000) -> list[str]:
    return textwrap.wrap(text, max_chars, break_long_words=False, break_on_hyphens=False)

def translate_chunk(chunk: str, target_lang="English")-> str:
    prompt = f"""
    You are a professional translator. Translate the text below into {target_lang}.
    - Keep the original meaning
    - Use a natural, coherent tone
    - Appropriate for academic/professional contexts
    The text is need to translate:
    {chunk}
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user", 
                "content": prompt
                }
            ]
        )
    print(response)
    return response.choices[0].message.content

def translate_file(input_path: str, output_path: str, target_lang="English"):
    text = read_file(input_path)
    chunks = split_into_chunks(text)
    results = []
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Translating part {i}/{len(chunks)}...")
        results.append(translate_chunk(chunk, target_lang))

    final_text = "\n\n".join(results)
    write_file(output_path, final_text)
    print(f"Translate done! and the file result path: {output_path}")

translate_file('./04-input-text.txt', './04-output-text.txt', 'English')
