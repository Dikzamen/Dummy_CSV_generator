import csv
from faker import Faker
from random import randint
from functools import partial
from task.celery import app

fake = Faker('en_US')


def sentences(lower, upper):
    number = randint(lower, upper)
    return ''.join(fake.sentences(number))


func_dict = {
    'Full name': fake.name,
    'Email': fake.email,
    'Phone number': fake.phone_number,
    'Text': sentences,
    'Integer': randint,
    'Address': fake.address,
    'Date': fake.date
}


@app.task
def create_func(query):
    range_type = ['Integer', 'Text']
    func_list = []
    for item in query:
        func = func_dict[item.type]
        if item.type in range_type:
            func = partial(func, item.range_lower, item.range_upper)
        func_list.append(func)
    return func_list


@app.task
def generate_data(file_id, num_rows, headers, func_lst, delimiter, quotechar):
    with open(f"media/table_{file_id}.csv", 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        writer = csv.writer(csvFile, delimiter=delimiter,
                            quotechar=quotechar)
        for i in range(num_rows):
            row = [func() for func in func_lst]
            writer.writerow(row)
