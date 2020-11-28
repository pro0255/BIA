import numpy as np
from algorithms.AbstractGenetic import AbstractGeneticAlgorithm
import copy
from solution.Solution import Solution
import random


class TeachingLearningBasedAlgorithm(AbstractGeneticAlgorithm):
    def __init__(self, **kwds):
        super().__init__(**kwds)

    def generate_population(self, Function):
        """Generates init population for alg. Individuals rand from random uniform.
        Args:
            Function (Function): Sphere Ackley..
        Returns:
            [Solution[]]: Generated population as array of Solutin class.
        """
        return [
            self.generate_individual(Function) for i in range(self.size_of_population)
        ]

    def generate_individual(self, Function):
        """Generates single individual. Method is used in generated population.
        Args:
            Function (Function): Sphere Ackley..
        Returns:
            [Solution]: Generated Solution class, where vector of parameters is populated with random uniform values in bounderies.
        """
        return self.generate_random_solution(Function.left, Function.right, self.D)

    def learning_phase(self, Function, students):
        """Represents learning phase in algorithm, where teachers ala best solution moves mean forward.
        Args:
            Function (Function): Sphere Ackley..
            students (Solution[]): Current population, group of students.
        """
        self.best_solution = self.select_best_solution(students)
        new_position = np.zeros(self.best_solution.dimension)
        new_position = self.calculate_difference(Function, students)
        new_position = np.clip(new_position, Function.left, Function.right)
        fV = Function.run(new_position)
        self.current_OFE += 1
        if fV < self.best_solution.fitness_value:
            self.best_solution.vector = new_position
            self.evaluate(self.best_solution, Function)

    def get_random_number(self):
        """Generates random number in uniform distribution (0,1) interval.
        Returns:
            [float]: Random uniform values.
        """
        return np.random.uniform()

    def calculate_difference(self, Function, students):
        """Calculates difference according to mean, random value uniform and random value tf.
        Args:
            Function (Function): Sphere Ackley..
            students (Solution[]): Whole pop represents students with teacher.
        Returns:
            [float[]]: Vector with in D.
        """
        r = self.get_random_number()
        Tf = np.random.randint(1, 3)
        return r * (self.best_solution.vector - Tf * self.calculate_mean(students))

    def get_random_student(self, to, students):
        """Get random student according to current one. Conditions is that i != j!
        Args:
            to (Solution): Current student.
            students (Solution[]): Whole pop represents students with teacher.
        Returns:
            [Solution]: Picked student from pop fulfilling condition.
        """
        random_s = random.choice(students)
        if random_s.key == to.key:
            return self.get_random_student(to, students)
        else:
            return random_s

    def learners_phase(self, Function, students):
        """Represents second phase in algorithm. Where every student learns from other one. Teacher included.
        Args:
            Function (Function): Sphere Ackley..
            students (Solution[]): Whole pop represents students with teacher.
        """
        for student in students:
            random_s = self.get_random_student(student, students)
            new_vector = np.zeros(student.dimension)
            if student.fitness_value < random_s.fitness_value:
                new_vector = student.vector + self.get_random_number() * (
                    student.vector - random_s.vector
                )
                new_vector = np.clip(new_vector, Function.left, Function.right)
            else:
                new_vector = student.vector + self.get_random_number() * (
                    random_s.vector - student.vector
                )
                new_vector = np.clip(new_vector, Function.left, Function.right)
            fV = Function.run(new_vector)
            self.current_OFE += 1
            if fV < student.fitness_value:
                student.vector = new_vector
                self.evaluate(student, Function)

    def calculate_mean(self, students):
        """Calculates mean in class.
        Args:
            students (Solution[]): Whole pop represents students.
        Returns:
            [type]: Mean in class
        """
        matrix = [student.vector for student in students]
        return np.mean(np.squeeze(matrix), axis=0)

    def start(self, Function):
        """Runs TeachingLearning Algorithm on specified Function, with specified args.
        Args:
            Function (class Function): specific Function (Sphere || Ackley..)
        """
        super().start()
        self.reset_alg()
        students = self.generate_population(Function)
        self.evalute_population(students, Function)
        while self.index_of_generation < self.max_generation and self.ofe_check():
            self.learning_phase(Function, students)
            self.learners_phase(Function, students)
            if self.graph:
                self.graph.draw(self.best_solution, students)
            self.index_of_generation += 1
            self.print_best_solution()
        return self.return_after_at_the_end(students)
