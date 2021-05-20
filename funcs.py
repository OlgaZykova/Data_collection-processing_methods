#Здесь описана функция, конвертирующая текст-описание зарплатных условий в словарь
def convert_text_to_dict(text):
    #инициализируем словарь зп пустыми значениями
    salary= {'from':None,'to':None,'cur':None}
    #удалим странные символы
    text=text.replace('\u202f','')
    text = text.replace('\xa0', '')
    #разделим текст на список
    text_split = text.split()
    #Инициализируем количество чисел в списке
    num_digits=0
    #инициализируем список чисел
    digits=[]
    #заполним список чисел
    for el in text_split:
        if el.isdigit():
            num_digits+=1
            digits.append(el)
    # если 2 числа, то есть информация и о мин, и о макс
    if num_digits ==2:
        salary['from']=digits[0]
        salary['to']=digits[1]
    # если 1, то только об одном значении
    if num_digits ==1:
        if text_split[0] == 'от.':
            salary['from']=digits[0]
        else:
            salary['to'] = digits[0]
    # последнее значение всегда валюта
    salary['cur'] = text_split[-1]
    return salary
#text = '1\u202f000 – 1\u202f500 бел.\xa0руб.'

#s = convert_text_to_dict(text)
#print(s)