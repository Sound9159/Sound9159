"""
Classes for the main in the Naive-Bayes Projects
"""

import csv
import os
from random import choices


class UI:

    def print_mass(self, mass):
        print(mass)

    def refer_input(self):
        """ input + validation for integer input
        Returns an integer if the user's input is valid, otherwise keep looping.
        @:param: mass - a massage you want the user to see
        """
        flag = True
        while flag:
            ans = self.bool_input('Would you like to enter a reference?')
            if ans:
                refer = input('Please insert reference:\n>> ')
                if os.path.exists(refer):
                    return refer
                self.print_mass('** ReferenceError: something is wrong with the file reference **')
            else:
                self.print_mass('** No reference entered **')
                return ans

    def int_input(self, mass: str) -> int:
        """ input + validation for integer input
        Returns an integer if the user's input is valid, otherwise keep looping.
        @:param: mass - a massage you want the user to see
        """
        while True:
            ans = input(mass+'\n>> ')
            if ans.isdigit():
                return int(ans)
            self.print_mass('** WrongInput: enter only positive integers **')

    def bool_input(self,mass: str) -> bool:
        """ input + validation for binary input
        @:param: mass - a massage you want the user to see
        @:return: True if the user's answer is positive, otherwise False.
        """
        while True:
            ans = input(mass+' [Yes/No]'+'\n>> ').lower()
            if ans in ['yes', 'no']:
                return ans == 'yes'
            self.print_mass('** WrongInput: enter only "Yes" or "No" **')


class DataFile:

    def __init__(self, ref, ui):
        self.ui = ui
        self.__DATA_raw = open(ref)
        self.names = tuple(next(csv.reader(self.__DATA_raw)))  # tuple of str
        self.DATA = list(csv.reader(self.__DATA_raw)).copy()  # list of lists
        self.__DATA_raw.close()
        self.__select_column()  # initiates by default column selection

    def __select_column(self):
        self.ui.print_mass('Here are all the attributes in your data:')
        for i in range(len(self.names)):
            print(i+1, "-", self.names[i])
        stop = False
        while not stop:
            ans = self.ui.int_input('How many attributes would you like to omit?')
            if ans:
                to_omit = []   # list of column number to omit
                self.ui.print_mass('Please select the columns you would like to omit')
                for i in range(ans):
                    to_omit.append(self.ui.int_input(f'Selection Number {i+1}:'))  # numbers from 1
                self.ui.print_mass('You chose to omit the following attributes:')
                for i in sorted(to_omit):
                    print(i, "-", self.names[i-1])
                stop = self.ui.bool_input('Do you confirm your choice?')
                if stop:
                    # columns deleting
                    subDATA = []  # list of rows as tuples
                    for row in self.DATA:
                        subDATA.append(
                            tuple(row[attr-1] for attr in range(1, len(self.names)+1) if attr not in to_omit)
                        )
                    # names deleting
                    self.names = tuple(self.names[attr-1] for attr in range(1, len(self.names)+1) if attr not in to_omit)
                    self.DATA = subDATA  # list of tuples
            else:
                stop = True
                # casting rows to tuple
                for row in range(len(self.DATA)):
                    self.DATA[row] = tuple(self.DATA[row])


class Classifier:

    def __init__(self, file, ui):
        self.ui = ui
        self.__data = file.DATA.copy()  # list of tuples
        self.N = len(self.__data)

    def set_classifier(self):
        """ sets all the information about the selected classifier in the data
        (1) self.class_ind - the classifier column number
        (2) self.class_vec - the column of the classifier
        (3) self.class_val - the unique values of the classifier
        :return: None
        """
        self.ui.print_mass('Please choose the classifier from the attributes list below:')
        for i in range(len(self.__data.names)):
            print(i + 1, "-", self.__data.names[i])
        self.class_ind = self.ui.int_input('') - 1  # the classifier index
        self.class_vec = [row[self.class_ind] for row in self.__data]  # the classifier column
        self.class_val = set(self.class_vec)  # the classifier unique values

    def set_train_test(self, p: float = 0.7):
        """
        Split the data to training-set and test-set as instance variables.
        (p*100)% of the data is assigned to the training-set.
        (1-p)*100% of the data is assigned to the test-set.
        :param p: a float, indicate the size of the training-set out of the data
        :return:
        """
        ind_dict = dict.fromkeys(self.class_val, [])
        for ind in range(self.N):
            ind_dict[self.class_vec[ind]].append(ind)
        train_ind = []
        for val in self.class_val:
            train_ind.extend(choices(ind_dict[val], k=round(p * len(ind_dict[val]))))
        self.train_set =[self.__data.DATA[ind] for ind in range(self.N) if ind in train_ind]
        self.test_set = [self.__data.DATA[ind] for ind in range(self.N) if ind not in train_ind]


    def probs(self):
        """ calculates all the conditional probabilities of the data
        :return dictionary of the unique rows as keys,
         and the value is a list of the probabilities."""
        pass


class NewRecord:
    pass


class Manager:

    def __init__(self):
        self.UI = UI()
        self.__ref = self.UI.refer_input()
        if self.__ref:
            self.__file = DataFile(self.__ref, self.UI)  # (.names , .DATA)
        else:
            self.UI.print_mass('Goodbye!')

    def get_data(self):
        return self.__file.DATA

    def get_name(self):
        return self.__file.names


def test():
         # refer1 = 'PlayTennis.csv'
         # refer2 = 'test_student_buy.csv'
         # refer3 = 'phishing_final.csv'  
         mng = Manager()
         print(mng.get_data()[0])

        
if __name__ == '__main__':
         test()



