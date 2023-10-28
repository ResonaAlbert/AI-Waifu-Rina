def use_questionlist(question_list):
    if question_list != []:
        status = True
        question = question_list[0]
        del question_list[0]
    else:
        status = False
        question = 'did not have question to ask!'
    return question

def update_questionlist(question_list, new_question):

    question_list.append(new_question)

    return question_list
