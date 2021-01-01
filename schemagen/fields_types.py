TYPE_FULL_NAME = 'FULL_NAME'
TYPE_JOB = 'JOB'
TYPE_SITY = 'Sity'

type_choice = [
            (TYPE_FULL_NAME, 'Full name'),
            (TYPE_JOB, 'Job'),
            (TYPE_SITY, 'Sity'),
        ]

type_list = [list(row)[1] for row in type_choice]
