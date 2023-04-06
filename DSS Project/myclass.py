import random
from globals import *

class Individual:
    def __init__(self, courses=None, credit=0):
        if courses is None:
            courses = []
        self.courses = courses
        self.credit = credit
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        fitness = 0
        fitness += self.mandatory_courses_check()
        fitness += self.basic_courses_check()
        fitness += self.indepth_courses_check()
        fitness += self.credit_check()
        fitness += self.course_bind_check()
        return fitness

    def mandatory_courses_check(self):
        global MANDATORY_COURSES
        cnt_mandatory_courses = 0
        for course in self.courses:
            for i in MANDATORY_COURSES:
                if course['course_name'] == i['course_name']:
                    cnt_mandatory_courses += 1
                    break
        if cnt_mandatory_courses < 31:
            return 31 - cnt_mandatory_courses
        return 0

    def basic_courses_check(self):
        global BASIC_COURSES
        cnt_basic_courses = 0
        for course in self.courses:
            for i in BASIC_COURSES:
                if course['course_name'] == i['course_name']:
                    cnt_basic_courses += 1
                    break
        if cnt_basic_courses < 5:
            return 5 - cnt_basic_courses
        return 0

    def indepth_courses_check(self):
        global INDEPTH_COURSES
        cnt_indepth_courses = 0
        for course in self.courses:
            for i in INDEPTH_COURSES:
                if course['course_name'] == i['course_name']:
                    cnt_indepth_courses += 1
                    break
        if cnt_indepth_courses < 6:
            return 6 - cnt_indepth_courses
        return 0

    def credit_check(self):
        global CREDITS
        if self.credit < CREDITS:
            return CREDITS - self.credit
        return 0

    def course_bind_check(self):
        global G
        sem_1, sem_2, sem_3, sem_4, sem_5, sem_6, sem_7, sem_8 = [], [], [], [], [], [], [], []
        count = 0
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
        fitness = 0
        index = 0
        for course in self.courses:
            id = course['id']
            if id not in list(G.nodes):
                continue
            ancestor_list = graph.get_ancestor_list(G, id)
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

    # One-point crossover
    def crossover(self, parent2):
        global NUM_COURSES
        crossover_point = random.randint(0, len(self.courses) - 1)
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

    # Combine 3 types of mutation (Scramble, Swap, Random)
    def mutate(self):
        global AVAILABLE_COURSES
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

        self.fitness = self.calc_fitness()
        return Individual(self.courses, self.credit)

