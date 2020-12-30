TYPE_FULL_NAME = 'FULL_NAME'
TYPE_JOB = 'JOB'

type_choice = [
            (TYPE_FULL_NAME, 'Full name'),
            (TYPE_JOB, 'Job'),
        ]

type_list = [list(row)[1] for row in type_choice]

#print(type_list)