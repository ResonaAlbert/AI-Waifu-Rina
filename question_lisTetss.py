question_list = []

question_list.append("What is the capital of France?")

print(question_list[0])

question_list.append("Hello?")

print(question_list[1])

question_list.append("How are you?")

del question_list[0]
print(question_list[0])
del question_list[0]
print(question_list[0])

del question_list[0]
if question_list == []:
    print("The list is empty")