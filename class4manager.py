"""
Classes for the main in the Naive-Bayes Project
"""

import csv  # for class DataFile
import os   # for class UI
from random import sample  # for class Classifier


class UI:

    def print_mass(self, mass):
        print(mass)

    def refer_input(self):
        """ input + validation for file reference
        @:return:  a file reference if the user's input is valid, otherwise False.
        """
        flag = True
        while flag:
            self.print_mass('Would you like to enter a reference?')
            ans = self.bool_input()
            if ans:
                refer = input('Please insert reference:\n>> ')
                if os.path.exists(refer):
                    return refer
                self.print_mass('** ReferenceError: something is wrong with the file reference **')
            else:
                self.print_mass('** No reference entered **')
                return ans

    def bool_input(self) -> bool:
        """ input + validation for binary input
        @:return: True if the user's answer is positive, otherwise False.
        """
        while True:
            ans = input('[Yes/No] ' + '>> ').lower()
            if ans in ['yes', 'no']:
                return ans == 'yes'
            self.print_mass('** WrongInput: enter only "Yes" or "No" **')

    def int_input(self) -> int:
        """ input + validation for integer input
                Returns an integer if the user's input is valid, otherwise keep looping.
                @:param: mass - a massage you want the user to see
                """
        while True:
            ans = input('>> ')
            if ans.isdigit():
                return int(ans)
            self.print_mass('** WrongInput: enter only positive integers **')

    def class_input(self, n: int) -> int:
        while True:
            ans = input('>> ')
            if ans.isdigit():
                if 1 <= int(ans) <= n:
                    return int(ans)-1
                self.print_mass('** WrongInput: column number out of range **')
            else:
                self.print_mass('** WrongInput: enter only positive integers **')

class DataFile:

    def __init__(self, ref):
        self.ui = UI()
        self.__DATA_raw = open(ref)
        self.names = tuple(next(csv.reader(self.__DATA_raw)))  # tuple of str
        self.DATA = list(csv.reader(self.__DATA_raw)).copy()  # list of lists
        self.__DATA_raw.close()
        self.__select_column()  # initiates by default column selection

    def __select_column(self):
        self.ui.print_mass('Here are all the attributes in your data:')
        for i in range(len(self.names)):
            print(i + 1, "-", self.names[i])
        stop = False
        while not stop:
            self.ui.print_mass('How many attributes would you like to omit?')
            ans = self.ui.int_input()
            if ans:
                to_omit = []  # list of column number to omit
                self.ui.print_mass('Please select the columns you would like to omit')
                for i in range(ans):
                    self.ui.print_mass(f'Selection Number {i + 1}:')  # numbers from 1
                    to_omit.append(self.ui.int_input())
                self.ui.print_mass('You chose to omit the following attributes:')
                for i in sorted(to_omit):
                    print(i, "-", self.names[i - 1])
                self.ui.print_mass('Do you confirm your choice?')
                stop = self.ui.bool_input()
                if stop:
                    # columns deleting
                    subDATA = []  # list of rows as tuples
                    for row in self.DATA:
                        subDATA.append(
                            tuple(row[attr-1] for attr in range(1, len(self.names) + 1) if attr not in to_omit)
                        )
                    # names deleting
                    self.names = tuple(
                        self.names[attr-1] for attr in range(1, len(self.names) + 1) if attr not in to_omit)
                    self.DATA = subDATA  # list of tuples
            else:
                stop = True
                # casting rows to tuple
                for row in range(len(self.DATA)):
                    self.DATA[row] = tuple(self.DATA[row])


class Classifier:

    def __init__(self, file):
        self.ui = UI()
        self.__data = file  # DataFile object
        self.N = len(self.__data.DATA)
        self.__set_classifier()
        self.__set_attr()
        self.__train_test()
        self.__probs()

    def __set_classifier(self):
        """ sets all the information about the selected classifier in the data
        (1) self.class_ind - the classifier column number
        (2) self.class_vec - the column of the classifier
        (3) self.class_val - the unique values of the classifier
        :return: None
        """
        self.ui.print_mass('Please choose the classifier from the attributes below:')
        for i in range(len(self.__data.names)):
            print(i + 1, "-", self.__data.names[i])
        self.class_ind = self.ui.class_input(len(self.__data.names))  # the classifier index
        self.class_vec = [row[self.class_ind] for row in self.__data.DATA]  # the classifier column
        self.class_val = set(self.class_vec)  # the classifier unique values

    def __set_attr(self):
        """ sets all the information about the attributes in the data
        (1) self.attr_ind - the classifier column number
        (2) self.attr_dict - the columns of the attributes as dictionary
        :return: None
        """
        self.attr_ind = [ind for ind in range(len(self.__data.names)) if ind != self.class_ind]
        self.attr_dict = dict(zip(self.attr_ind, [[] for i in self.attr_ind]))
        for col in self.attr_ind:
            for row in self.__data.DATA:
                self.attr_dict[col].append(row[col])

    def __train_test(self, p: float = 0.7):
        """
        Split the data to training-set and test-set as instance variables.
        (1) self.ind_dict - dict of class values as keys, and a list of their indexes in the data as values
        (2) self.train_data - (p*100)% of the data
        (3) self.test_data - (1-p)*100% of the data
        :param p: a float, indicate the size of the training-set out of the data
        """
        self.ind_dict = dict(zip(self.class_val, [[] for i in self.class_val]))
        for ind in range(self.N):
            self.ind_dict[self.class_vec[ind]].append(ind)
        train_ind = []
        for val in self.class_val:
            train_ind.extend(sample(self.ind_dict[val], k=round(p * len(self.ind_dict[val]))))
        self.train_data = [self.__data.DATA[ind] for ind in train_ind]
        self.test_data = [self.__data.DATA[ind] for ind in range(self.N) if ind not in train_ind]

    def __probs(self):
        """ calculates all the conditional probabilities of the training-set
        :return dictionary of the unique rows as keys,
         and the value is a list of the probabilities."""
        train_n = dict(zip(self.class_val,
                                   [sum(row[self.class_ind] == val for row in self.train_data) for val in self.class_val]))
        # P(C_i)
        self.prob_class = dict(zip(self.class_val,
                                   [train_n[val] / len(self.train_data) for val in self.class_val]))
        # P(X|C_i)
        self.prob_attr = {}
        for attr in self.attr_ind:
            self.prob_attr[attr] = {}
            for cl in self.class_val:
                self.prob_attr[attr][cl] = {}
                for val in set(self.attr_dict[attr]):
                    self.prob_attr[attr][cl][val] = \
                        sum(row[attr] == val and row[self.class_ind] == cl for row in self.train_data) \
                        / train_n[cl]
                # laplacian correction
                if 0 in self.prob_attr[attr][cl].values():
                    for val in self.prob_attr[attr][cl]:
                        self.prob_attr[attr][cl][val] = (self.prob_attr[attr][cl][val]*train_n[cl] + 1) \
                                                        / (train_n[cl] + len(self.prob_attr[attr][cl]))


class NewRecord:

    def __init__(self, record, classifier, is_cl: bool = True):
        self.record = record
        self.cl = record[classifier.class_ind]
        self.__classifier = classifier
        if self.__rec_validation(is_cl):
            self.__pred()
        else:
            self.pred = False

    def __rec_validation(self, is_cl) -> bool:
        if type(self.record) in [tuple, list]:
            if len(self.record) == len(self.__classifier.attr_ind)+is_cl:
                record1 = list(self.record)
                if not is_cl:
                    record1.insert(self.__classifier.class_ind, 'NA')
                for attr in self.__classifier.attr_ind:
                    if record1[attr] not in \
                            self.__classifier.prob_attr[attr][self.__classifier.class_vec[0]]:
                        self.__classifier.ui.print_mass('** WrongInput: attributes values don\'t exist **')
                        return False
                return True
            self.__classifier.ui.print_mass('** WrongInput: record\'s length is wrong **')
            return False
        self.__classifier.ui.print_mass('** WrongInput: record must be a list or a tuple **')
        return False

    def __pred(self):
        self.pred_dict = self.__classifier.prob_class
        # P(X|C_i)*P(C_i)
        for attr in self.__classifier.prob_attr:
            for cl in self.pred_dict:
                self.pred_dict[cl] *= self.__classifier.prob_attr[attr][cl][self.record[attr]]
        self.pred = sorted(self.pred_dict, key=lambda x: self.pred_dict[x])[-1]


class Manager:

    def __init__(self):
        self.UI = UI()
        self.__ref = self.UI.refer_input()
        if self.__ref:
            self.__file = DataFile(self.__ref)  # (.names , .DATA)
            self.classifier = Classifier(self.__file)
        else:
            self.UI.print_mass('Goodbye!')

    def get_data(self):
        return self.__file.DATA

    def get_name(self):
        return self.__file.names

    def accuracy(self, data: list):
        ls1 = []
        correct = 0
        for row in data:
            foo = NewRecord(row, self.classifier).pred
            if foo:
                ls1.append(foo)
                correct += foo == row[self.classifier.class_ind]
            else:
                return
        ACR = correct/len(data)
        return ACR, ls1


def test():
    """
    print('\n############ Basic Example ############')
    cl1 = Classifier(DataFile('PlayTennis.csv'))
    print('\n#### Training-Set ####')
    for row in cl1.train_data:
        print(row)
    print('\n#### Test-Set ####')
    for row in cl1.test_data:
        print(row)
    print('\n#### P(C_i) ####')
    for item in cl1.prob_class.items():
        print(item)
    print('\n#### P(X|C_i) With Laplacian Correction ####')
    for item in cl1.prob_attr.items():
        print(item)
    print('\n#### P(C_i|X) ; X=(No, FALSE, High, Hot, Sunny) ####')
    new_rec = NewRecord(('No', 'FALSE', 'High', 'Hot', 'Sunny'), cl1)
    print(new_rec.pred_dict)
    print('Prediction :', new_rec.pred, '=?=', new_rec.pred, ':', 'Outcome')
    # ('No', 'FALSE', 'High', 'Hot')
    print('\n\n')
    # """
    # """
    print('\n############ Without "Outlook" ############')
    print('###### "Temperature" as the Outcome ######')
    print('############ SAY WHAAAAAT ??? ############')
    cl2 = Classifier(DataFile('PlayTennis.csv'))
    print('\n#### Training-Set ####')
    for row in cl2.train_data:
        print(row)
    print('\n#### Test-Set ####')
    for row in cl2.test_data:
        print(row)
    print('\n#### P(C_i) ####')
    for item in cl2.prob_class.items():
        print(item)
    print('\n#### P(X|C_i) With Laplacian Correction ####')
    for item in cl2.prob_attr.items():
        print(item)
    new_rec = NewRecord(('No', 'FALSE', 'High', 'Hot'), cl2)
    print('\n#### P(C_i|X) ; X=(No, FALSE, High, Hot, Sunny) ####')
    print(new_rec.pred_dict)
    print('Prediction :', new_rec.pred, '=?=', new_rec.pred, ':', 'Outcome')
    # """


if __name__ == '__main__':
    test()
