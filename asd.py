from openai import OpenAI

client = OpenAI(api_key="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")

query = "sf영화 추천해줘"

response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "system",
            "content": "너는 영화를 추천해주는 AI야.",
        },
        {"role": "user", "content": query},
    ],
)
print(response.choices[0].message.content)
