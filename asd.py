from openai import OpenAI

client = OpenAI(api_key="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")

query = "인셉션을 재미있게 봤어 비슷한 영화를 추천해줘 매트릭스 말고"

response0 = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "system",
            "content": "역할: 영화 평론가, 작업: 제목과 1점에서 10점사이의 추천도와 추천이유를 제공하여 사용자에게 영화를 추천하고, 선택 항목은 지난 30년간의 영화이며 TV 시리즈가 포함되지 않도록 합니다.",
        },
        {"role": "user", "content": query},
    ],
)


messages = [{"role": "user", "content": response0.choices[0].message.content}]
function1 = [
    {
        "name": "get_movie_title",
        "description": "영화의 제목을 찾아서 알려줍니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "movie_title": {
                    "type": "string",
                    "description": "영화이름 eg. 레옹, 대부, 인터스텔라",
                },
            },
            "required": ["movie_title"],
        },
    }
]
function2 = [
    {
        "name": "get_movie_star",
        "description": "영화의 점수를 찾아서 알려줍니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "movie_star": {
                    "type": "string",
                    "description": "영화점수 eg. 10/10, 9/10, 5/10, 6점",
                },
            },
            "required": ["movie_star"],
        },
    }
]



response1 = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=function1,
    function_call="auto",
    )

response2 = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=function2,
    function_call="auto",
    )

response_message1 = response1.choices[0].message
response_message2 = response2.choices[0].message

print(response0.choices[0].message.content)
print(response_message1)
print(response_message2)
