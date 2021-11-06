"""
Naive-Bayes Classification Project
If you give as data, we will give you knowledge.
And as F. Bacon said  - "Knowledge is Power"
"""
from class4manager import *


def main():
    # """
    print('########### Are You Excited as We Are ?? ###########')
    print('\n#################### Small Data ####################')
    manager1 = Manager()  # test_student_buy.csv
    ac_train1 = manager1.accuracy(manager1.classifier.train_data)
    print("\n+------------------------------------------+",
          f"| The Accuracy of the Training-set is: {round(ac_train1[0] * 100)}% |",
          "+------------------------------------------+",
          sep='\n')
    print("#### Prediction Vector ####")
    print(ac_train1[1])
    print('#### Training-Set ####')
    for row in manager1.classifier.train_data:
        print(row)
    ac_test1 = manager1.accuracy(manager1.classifier.test_data)
    print("\n+------------------------------------------+",
          f"| The Accuracy of the Test-set is: {round(ac_test1[0] * 100)}%     |",
          "+------------------------------------------+",
          sep='\n')
    print("#### Prediction Vector ####")
    print(ac_test1[1])
    print('######## Test-Set #########')
    for row in manager1.classifier.test_data:
        print(row)
    # """
    """
    print('\n\n')
    print('\n#################### Large Data ####################')
    manager2 = Manager()  # phishing_final.csv
    ac_train2 = manager2.accuracy(manager2.classifier.train_data)
    print("\n+------------------------------------------+",
          f"| The Accuracy of the Training-set is: {round(ac_train2[0] * 100)}% |",
          "+------------------------------------------+",
          sep='\n')
    ac_test2 = manager2.accuracy(manager2.classifier.test_data)
    print("\n+------------------------------------------+",
          f"| The Accuracy of the Test-set is: {round(ac_test2[0] * 100)}%     |",
          "+------------------------------------------+",
          sep='\n')
    # """


if __name__ == '__main__':
    main()
