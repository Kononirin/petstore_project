import json

string_as_json_format = '{"answer": "Hello, User"}'
obj_answer = json.loads(string_as_json_format)
print(obj_answer['answer'])

key = "answer"

if key in obj_answer:
    print(obj_answer[key])
else:
    print(f"Ключа {key} в JSON нет")