
import random
import json
import time
import graphTest

# TODO: Define a list of available courses
AVAILABLE_COURSES = []
MANDATORY_COURSES = []
BASIC_COURSES = []
INDEPTH_COURSES = []
UNBOUND_COURSES_ID = [11, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 23, 28]
UNBOUND_COURSES = []

# Define the number of courses to recommend to each student
NUM_COURSES = 42

# Define the number of credits required for graduation
CREDITS = 128

# Define the population size
POP_SIZE = 500
NUM_GENERATIONS = 10000

# Define the probability of mutation
MUTATION_PROB = 0.1

# Define graph
G = graphTest.create_graph()

class Individual:

    def __init__(self, courses=None, credit=0):
        if courses is None:
            courses = []
        self.courses = courses
        self.credit = credit
        self.fitness = self.calc_fitness()

    # TODO: Calculate fitness (might have to add weight)
    def calc_fitness(self):
        global MANDATORY_COURSES
        global BASIC_COURSES
        global INDEPTH_COURSES
        global CREDITS

        fitness = 0
        cnt_mandatory_courses = 0
        cnt_basic_courses = 0
        cnt_indepth_courses = 0
        for course in self.courses:
            flag = False
            for i in MANDATORY_COURSES:
                if course['course_name'] == i['course_name']:
                    cnt_mandatory_courses += 1
                    flag = True
                    break
            if flag:
                continue
            for i in BASIC_COURSES:
                if course['course_name'] == i['course_name']:
                    cnt_basic_courses += 1
                    flag = True
                    break
            if flag:
                continue
            for i in INDEPTH_COURSES:
                if course['course_name'] == i['course_name']:
                    cnt_indepth_courses += 1
                    break

        # TODO: Add more bound conditions
        #  1. So tin chi phai >= 128
        #  2. So tin chi cua cac mon bat buoc phai >= 31
        #  3. So tin chi cua cac mon co ban phai >= 5
        #  4. So tin chi cua cac mon chuyen nganh phai >= 6
        if cnt_mandatory_courses < 31:
            fitness += 31 - cnt_mandatory_courses
        if cnt_basic_courses < 5:
            fitness += 5 - cnt_basic_courses
        if cnt_indepth_courses < 6:
            fitness += 6 - cnt_indepth_courses
        if self.credit < CREDITS:
            fitness += CREDITS - self.credit
        fitness += self.course_bind_check()
        return fitness

    def course_bind_check(self):
        global G
        sem_1, sem_2, sem_3, sem_4, sem_5, sem_6, sem_7, sem_8 = [], [], [], [], [], [], [], []
        count = 0
        fitness = 0
        for course in self.courses:
            if count < 6:
                sem_1.append(course)
            elif count < 12:
                sem_2.append(course)
            elif count < 18:
                sem_3.append(course)
            elif count < 24:
                sem_4.append(course)
            elif count < 30:
                sem_5.append(course)
            elif count < 35:
                sem_6.append(course)
            elif count < 40:
                sem_7.append(course)
            else:
                sem_8.append(course)
            count += 1


        index = 0
        for course in self.courses:
            id = course['id']
            if id not in list(G.nodes):
                continue
            ancestor_list = graphTest.get_ancestor_list(G, id)
            if index < 6:
                if not len(ancestor_list) == 1:
                    fitness += 1
            elif index < 12:
                for ancestor_id in ancestor_list:
                    if ancestor_id == 0:
                        continue
                    flag = False
                    for crs in sem_1:
                        if crs['id'] == ancestor_id:
                            flag = True
                            break
                    if not flag:
                        fitness += 1
            elif index < 18:
                for ancestor_id in ancestor_list:
                    if ancestor_id == 0:
                        continue
                    flag = False
                    for crs in sem_1 + sem_2:
                        if crs['id'] == ancestor_id:
                            flag = True
                            break
                    if not flag:
                        fitness += 1
            elif index < 24:
                for ancestor_id in ancestor_list:
                    if ancestor_id == 0:
                        continue
                    flag = False
                    for crs in sem_1 + sem_2 + sem_3:
                        if crs['id'] == ancestor_id:
                            flag = True
                            break
                    if not flag:
                        fitness += 1
            elif index < 30:
                for ancestor_id in ancestor_list:
                    if ancestor_id == 0:
                        continue
                    flag = False
                    for crs in sem_1 + sem_2 + sem_3 + sem_4:
                        if crs['id'] == ancestor_id:
                            flag = True
                            break
                    if not flag:
                        fitness += 1
            elif index < 35:
                for ancestor_id in ancestor_list:
                    if ancestor_id == 0:
                        continue
                    flag = False
                    for crs in sem_1 + sem_2 + sem_3 + sem_4 + sem_5:
                        if crs['id'] == ancestor_id:
                            flag = True
                            break
                    if not flag:
                        fitness += 1
            elif index < 40:
                for ancestor_id in ancestor_list:
                    if ancestor_id == 0:
                        continue
                    flag = False
                    for crs in sem_1 + sem_2 + sem_3 + sem_4 + sem_5 + sem_6:
                        if crs['id'] == ancestor_id:
                            flag = True
                            break
                    if not flag:
                        fitness += 1
            index += 1

        sem_8_course = [temp['course_name'] for temp in sem_8]
        if 'Graduation Thesis' not in sem_8_course:
            fitness += 1
        return fitness

    # TODO: One-point crossover
    def crossover(self, parent2):
        # Choose a random crossover point
        crossover_point = random.randint(0, len(self.courses) - 1)
        # Create a child by combining the parents' courses up to the crossover point
        child_course = self.courses[:crossover_point]
        if len(child_course) < NUM_COURSES:
            for course in parent2.courses:
                if len(child_course) == NUM_COURSES:
                    break
                if course not in child_course:
                    child_course.append(course)
        child_credit = 0
        for course in child_course:
            child_credit += course['credits']
        return Individual(child_course, child_credit)

    # TODO: Might have to take a look at this (Scramble mutation)
    def mutate(self):
        num = random.randint(1, 3)
        if self.fitness >= 1:
            index = 0
            for course in self.courses:
                if course['course_name'] == 'Graduation Thesis':
                    index = self.courses.index(course)
                    break
            self.courses[index], self.courses[-1] = self.courses[-1], self.courses[index]
        if num == 1:
            # Choose a random mutation point
            mutation_start_point = random.randint(0, len(self.courses) - 2)
            mutation_end_point = random.randint(mutation_start_point + 1, len(self.courses) - 1)

            # Choose a random course to replace the course at the mutation point
            shuffled_list = random.sample(self.courses[mutation_start_point:mutation_end_point], len(self.courses[mutation_start_point:mutation_end_point]))
            self.courses[mutation_start_point:mutation_end_point] = shuffled_list
        elif num == 2:
            count = random.randint(1, 3)
            while count > 0:
                p1 = random.randint(0, len(self.courses) - 1)
                p2 = random.randint(0, len(self.courses) - 1)
                self.courses[p1], self.courses[p2] = self.courses[p2], self.courses[p1]
                count -= 1
        else:
            course = random.choice(self.courses)
            self.courses.remove(course)
            rand_course = random.choice(AVAILABLE_COURSES)
            while rand_course in self.courses:
                rand_course = random.choice(AVAILABLE_COURSES)
            self.courses.append(rand_course)

        # Recalculate the fitness of the individual
        self.fitness = self.calc_fitness()
        return Individual(self.courses, self.credit)

# TODO: Define a function to add courses to the available courses list
def adding_courses():
    global AVAILABLE_COURSES
    global MANDATORY_COURSES
    global BASIC_COURSES
    global INDEPTH_COURSES
    global UNBOUND_COURSES
    global UNBOUND_COURSES_ID
    with open('courses/mandatory_courses.json') as f:
        data = json.load(f)
        for i in data:
            AVAILABLE_COURSES.append(i)
            MANDATORY_COURSES.append(i)
            if i['id'] in UNBOUND_COURSES_ID:
                UNBOUND_COURSES.append(i)
    with open('courses/basic_knowledge_courses.json') as f:
        data = json.load(f)
        for i in data:
            AVAILABLE_COURSES.append(i)
            BASIC_COURSES.append(i)
            if i['id'] in UNBOUND_COURSES_ID:
                UNBOUND_COURSES.append(i)
    with open('courses/indepth_knowledge_courses.json') as f:
        data = json.load(f)
        for i in data:
            AVAILABLE_COURSES.append(i)
            INDEPTH_COURSES.append(i)
            if i['id'] in UNBOUND_COURSES_ID:
                UNBOUND_COURSES.append(i)
    # for course in AVAILABLE_COURSES:
    #     print(course)

# TODO: Define a function to generate a population
def generate_population():
    global POP_SIZE
    global CREDITS
    global AVAILABLE_COURSES
    global MANDATORY_COURSES
    global BASIC_COURSES
    global INDEPTH_COURSES
    global NUM_COURSES
    global UNBOUND_COURSES
    # Create an empty list to hold the population
    population = []
    # Iterate over the population size
    for i in range(POP_SIZE):
        # Create a new individual as a list of randomly selected courses
        courses = []
        credit = 0
        # for x in UNBOUND_COURSES:
        #     courses.append(x)
        #     credit += x['credits']

        # Iterate over the number of courses to recommend
        while len(courses) < NUM_COURSES - 1:
            rand_course = random.choice(AVAILABLE_COURSES)
            # Ensure that the course is not already in the courses list
            while rand_course in courses:
                rand_course = random.choice(AVAILABLE_COURSES)
            courses.append(rand_course)
            credit += rand_course['credits']

        courses.append(MANDATORY_COURSES[30])
        credit += MANDATORY_COURSES[30]['credits']
        # Append the individual to the population list
        population.append(Individual(courses, credit))
    # Return the population
    return population

# TODO: Define the genetic algorithm function
def genetic_algorithm():
    global NUM_GENERATIONS
    global POP_SIZE
    global MUTATION_PROB
    # Generate the initial population
    population = generate_population()
    found = False
    loop_num = 0
    # Iterate over each generation
    while not found:
        loop_num += 1
        # TODO: Selection
        population = sorted(population, key=lambda x: x.fitness)

        if population[0].fitness == 0:
            found = True
            break

        new_generation = []

        s = (len(population) * 10) // 100
        new_generation.extend(population[:s])

        s = (len(population) * 90) // 100
        half = len(population) * 50 // 100

        for _ in range(s):
            # TODO: Crossover for the first half of the population
            parent1 = random.choice(population[:half])
            parent2 = random.choice(population[:half])
            child = parent1.crossover(parent2)

            # TODO: Mutation
            rand_num = random.random()
            if rand_num <= MUTATION_PROB:
                child = child.mutate()
            new_generation.append(child)

        population = new_generation
        avg_fitness = 0
        for individual in population:
            avg_fitness += individual.fitness
        avg_fitness = avg_fitness / len(population)

        print()
        print("Best individual in the final population: ")
        course_list = []
        for course in population[0].courses:
            course_list.append(course['course_name'])
        print(course_list)
        print("Fitness: " + str(population[0].fitness))
        print("Fitness average: " + str(avg_fitness))
        print("Loop number: " + str(loop_num))

    print()
    print("Best individual in the final population: ")
    sem_1, sem_2, sem_3, sem_4, sem_5, sem_6, sem_7, sem_8 = [], [], [], [], [], [], [], []
    count = 0
    for course in population[0].courses:
        if count < 6:
            sem_1.append(course['course_name'])
        elif count < 12 :
            sem_2.append(course['course_name'])
        elif count < 18 :
            sem_3.append(course['course_name'])
        elif count < 24 :
            sem_4.append(course['course_name'])
        elif count < 30 :
            sem_5.append(course['course_name'])
        elif count < 35 :
            sem_6.append(course['course_name'])
        elif count < 40 :
            sem_7.append(course['course_name'])
        else :
            sem_8.append(course['course_name'])
        count += 1
    print("Semester 1: " + ', '.join(sem_1))
    print("Semester 2: " + ', '.join(sem_2))
    print("Semester 3: " + ', '.join(sem_3))
    print("Semester 4: " + ', '.join(sem_4))
    print("Semester 5: " + ', '.join(sem_5))
    print("Semester 6: " + ', '.join(sem_6))
    print("Semester 7: " + ', '.join(sem_7))
    print("Semester 8: " + ', '.join(sem_8))

def main():
    start = time.time()
    adding_courses()
    genetic_algorithm()
    end = time.time()
    print()
    print("Time: " + str(end - start))

if __name__ == "__main__":
    main()

