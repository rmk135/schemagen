
import random
import string

companies = ['Planteks', 'Google', 'Fazan' ]
professions = ['Developer', 'Software Engineer', 'Tech Lead', 'Team Lead']

def phone_number():
    numbers = string.digits
    phone = '+ ' + ''.join(random.choice(numbers) for i in range(3))+ ' '+ ''.join(random.choice(numbers) for i in range(7))
    return phone

def name_gen():
    names = ["Roman", "Vera", "Paulo"]
    familes = ["Mogylatov", "Vovk", "Mask"]

    name = random.choice(names) + ' ' + random.choice(familes)
    return name

def job_gen():
    job = random.choice(professions) + ' at ' + random.choice(companies)
    return job

def sity_gen():
    sities = ["NY", "Kiev", "Huston"]
    town = random.choice(sities)
    return town
