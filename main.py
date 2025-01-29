from groq import Groq

client = Groq(api_key="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")

completion = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[{
        "role":"system",
        "content":"You are an islamic scholar who has read whole quran and all the authentic hadiths and knows everything about islam and Allah. You don't know about anything apart from Quran and Hadiths."
    },
    {
        "role":"user",
        "content":f"{user_input}"
    }],
    temperature=0.6,
    max_completion_tokens=4096,
    top_p=0.95,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
