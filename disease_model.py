import random
def infect(infect_chance:float)->bool:
    """accepts a number between 0 and 1 and compares it to randomly generated
        value between 0 and 1 to return boolean values indicating if infection has occured"""
    if infect_chance>random.uniform(0,1):
       return True
    return False

def recover(recover_chance:float)->bool:
    """takes a float between 0 and 1 and compares it to a randomly generated
value between 0 and 1 to return boolean values indicateing if the patient recovered"""
    if recover_chance>random.uniform(0,1):
        return True
    return False
def  contact_indices(pop_size:int,source:int,contact_range:int):
    """takes three arguments as integers and returns a list of indices to indicate which people
came in contact with an infected person"""
    contact_list = []
    for index in range(source - contact_range, source + contact_range + 1):
        if index >= 0 and index < pop_size:
            contact_list.append(index)
    return contact_list

def apply_recoveries(population: list,recover_chance: float) -> None:
    """takes a list of strings and float value and iterates through the list and
    determines recovery probability for infected individuals"""
    for index in range(len(population)):
        if population[index] == 'I' and recover(recover_chance):
            population[index] = 'R'

def contact(population: list, source: int, contact_range: int, infect_chance: float) -> None:
    """Takes a list of strings, index of infected person, integer indicating contact range and infection
    probability of disease to determine infected individuals in the population """
    contact_list = contact_indices(len(population), source, contact_range)
    for index in contact_list:
        if population[index] == 'S' and infect(infect_chance):
            population[index] = 'I'

def apply_contacts(population: list, contact_range: int, infect_chance: float) -> None:
    """Simulate all of the infected people in the population coming into contact with other people"""
    infect_list = []
    for index in range(len(population)):
        if population[index] == 'I':
            infect_list.append(index)
            
    for index in infect_list:
        contact(population, index, contact_range, infect_chance)

def population_SIR_counts(population: list) -> dict:
    """takes a list of strings of population and returns a dictionary of counts"""
    return {"susceptible": population.count('S'), "infected": population.count('I'), "recovered": population.count('R')}

def simulate_day(population: list, contact_range: int, infect_chance: float, recover_chance: float):
    """takes a list of strings, an integer and a float to simulate one day in the progression of the disease"""
    apply_recoveries(population, recover_chance)
    apply_contacts(population, contact_range, infect_chance)

def initialize_population(pop_size:int) -> list:
    """Initialize the state of the population"""
    population = ['S'] * pop_size # to show everyone was susceptible on the first day
    population[0] = 'I' # Exclude the first person who was infected
    return population

def simulate_disease(pop_size:int, contact_range:int, infect_chance:float, recover_chance:float) -> list:
    """Simulate one day in the progression of the disease"""
    population = initialize_population(pop_size)
    counts = population_SIR_counts(population)
    all_counts = [counts] # a list containing the states of each day during the outbreak
    while counts['infected'] > 0:
        simulate_day(population, contact_range, infect_chance, recover_chance)
        counts = population_SIR_counts(population)
        all_counts.append(counts)
    return all_counts

def peak_infections(all_counts:list) -> int:
    """Find the peak infection"""
    max_infections = 0
    for day in all_counts:
        if day['infected'] > max_infections:
            max_infections = day['infected']
    return max_infections
        
def display_results(all_counts:list) -> None:
    """Display the state of each day in the progression of the disease"""
    num_days = len(all_counts)
    print("Day".rjust(12) + "Susceptible".rjust(12) + "Infected".rjust(12) + "Recovered".rjust(12)) # print the result in a table format
    for day in range(num_days):
        line = str(day).rjust(12)
        line += str(all_counts[day]["susceptible"]).rjust(12)
        line += str(all_counts[day]["infected"]).rjust(12)
        line += str(all_counts[day]["recovered"]).rjust(12)
        print(line)
    print("\nPeak Infections: {}".format(peak_infections(all_counts)))
