"""

"""

import csv
import os
from random import choices

# refer1 = r'C:\Users\Tzlil\Desktop\Tech-Career\Projects\OOP_Bayes_Classification\PlayTennis.csv'
# refer2 = r'C:\Users\Tzlil\Desktop\Tech-Career\Projects\OOP_Bayes_Classification\test_student_buy.csv'
# refer3 = r'C:\Users\Tzlil\Desktop\Tech-Career\Projects\OOP_Bayes_Classification\phishing_final.csv'


class UX:

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
                    return refer   #??   input: r'c:\fgh'
                self.print_mass('** ReferenceError: something is wrong with the file reference **')
            else:
                self.print_mass('** No reference entered **')
                return ans

    def int_input(self,mass: str) -> int:
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

    def __init__(self, ref, ux):
        self.ux = ux
        self.__DATA_raw = open(ref)
        self.names = tuple(next(csv.reader(self.__DATA_raw)))
        self.DATA = list(csv.reader(self.__DATA_raw)).copy()
        self.__DATA_raw.close()
        self.__select_column()

    def __select_column(self):
        self.ux.print_mass('Here are all the attributes in your data:')
        for i in range(len(self.names)):
            print(i+1,"-",self.names[i])
        stop = False
        while not stop:
            ans = self.ux.int_input('How many attributes would you like to omit?')
            if ans:
                to_omit = []   # list of column number to omit
                self.ux.print_mass('Please select the columns you would like to omit')
                for i in range(ans):
                    to_omit.append(self.ux.int_input(f'Selection Number {i+1}:'))  # numbers from 1
                self.ux.print_mass('You chose to omit the following attributes:')
                for i in sorted(to_omit):
                    print(i, "-", self.names[i-1])
                stop = self.ux.bool_input('Do you confirm your choice?')
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

    def __init__(self, file, ux):
        self.ux = ux
        self.__data = file.DATA
        self.N = len(self.__data.DATA)

    def set_classifier(self):
        self.ux.print_mass('Please choose the classifier from the attributes list below:')
        for i in range(len(self.__data.names)):
            print(i + 1, "-", self.__data.names[i])
        self.class_ind = self.ux.int_input('') - 1  # the classifier index
        self.class_vec = [row[self.class_ind] for row in self.__data.DATA]  # the outcome column
        self.class_val = set(self.class_vec)

    def set_train_test(self, p: float = 0.7):
        """
        Split the data to training-set and test-set as instance variables.
        (p*100)% of the data is assigned to the training-set.
        (1-p)*100% of the data is assigned to the test-set.
        :param p: a float, indicate the sixe of the training-set out of the data
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



    def set_probs(self):
        """ calculates all the conditional probabilities of the data
        :return dictionary of the unique rows as keys,
         and the value is a list of the probabilities."""
        # self.prob_class = dict.fromkeys(self.class_val, )



class NewRecord:
    pass


class Manager:

    def __init__(self):
        self.UX = UX()
        self.__ref = self.UX.refer_input()
        if self.__ref:
            self.__file = DataFile(self.__ref, self.UX)  # (.names , .DATA)
        else:
            self.UX.print_mass('Goodbye!')

    def get_data(self):
        return self.__file.DATA

    def get_name(self):
        return self.__file.names


# C:\Users\Tzlil\Desktop\Tech-Career\Projects\OOP_Bayes_Classification\PlayTennis.csv
mng = Manager()
print(mng.get_data())




