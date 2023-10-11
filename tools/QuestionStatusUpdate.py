def use_questionlist0(question_list):

    status = True
    if question_list[0][0] == True:
        #ask_text = '1'
        question_list[0][0] = False
        question = question_list[0][1]
        if question_list[1][0] == True:
            question_list[0][1] = question_list[1][1]
            question_list[1][0] = False

    else:
        status = False
        question = 'did not have question to ask!'

    return [status, question]

def update_questionlist0(question_list, new_question):

    if question_list[0][0] == False:
        question_list[0][1] = new_question
        question_list[0][0] = True
    else:
        question_list[1][1] = new_question
        question_list[1][0] = True
    return question_list

def use_questionlist(question_list):

    if question_list != []:
        status = True
        question = question_list[0]
        del question_list[0]
    else:
        status = False
        question = 'did not have question to ask!'

    return [status, question]

def update_questionlist(question_list, new_question):

    question_list.append(new_question)

    return question_list
