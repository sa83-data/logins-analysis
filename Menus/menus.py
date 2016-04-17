"""
    Given number of cuisines, and number of dishes in each cuisine, list all possible menus as output.
    A menu contains exactly one dish from each cuisine and all cuisines must be included.
    Cuisines are indicated by letters and dishes by numbers.
    Needs numpy and pandas installed.
"""

import sys
import numpy as np
import pandas as pd
from numpy.core.defchararray import add as chararray_add

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z']


def usage():
    print("Incorrect usage of program from command line. Use as follows.")
    print
    print("Description:")
    print("   Given list of number of dishes per cuisine, lists all possible menus.")
    print("   A menu contains exactly one dish from each cuisine and all cuisines must be included.")
    print("   Cuisines are indicated by letters and dishes by numbers.")
    print("   Needs numpy==1.10.4 and pandas==0.18.0 installed.")
    print
    print("Usage:")
    print("   python menus.py dishes1 dishes2 ...")
    print("   Example: python menus.py 3 4 5 6")
    print("   In this example, we have 4 cuisines, each with 3, 4, 5 and 6 dishes.")
    print
    print("Notes:")
    print("   Maximum number of cuisines i.e. length of list of dishes allowed is %d." % len(LETTERS))
    print("   Number of (non-zero) dishes for a minimum of 1 cuisine is required.")
    print("   Floating point numbers will be rounded to nearest integer.")
    print("   Cuisines with 0 dishes will be skipped.")
    print
    sys.exit(-1)


def array_cross_product(a1, a2, sep=' '):
    """
    Returns cross-product of elements of two arrays.
    :param a1: First input array
    :param a2: Second input array
    :param sep: Character to separate elements by. Default is space.
    :return:
    """
    # repeat each element in a1 equal to length of a2
    a1_rep = np.repeat(a1, len(a2))

    # tile-repeat a2 equal to length of a1
    a2_rep = np.tile(a2, len(a1))

    # repeat separator equal to product of lengths of a1 and a2
    sep_rep = np.repeat(sep, len(a1) * len(a2))

    return chararray_add(chararray_add(a1_rep, sep_rep), a2_rep)


def main(args):
    """
    Scripting wrapper for menu generation program.
    :param args: Pass through arguments from command line
    """

    # ensure number of dishes for at least one cuisine is passed
    global LETTERS
    if len(args) < 2:
        usage()

    # parse command line arguments
    dishes_per_cuisine = np.array(args[1:]).astype(int)

    # check for zeros
    if all(np.zeros(len(dishes_per_cuisine)) == dishes_per_cuisine):
        print
        print("All cuisines seem to have zero dishes.")
        print("No menus to generate.")
        print
        sys.exit(-1)

    # at least one cuisine has non-zero number of dishes
    # check for and remove any existing zeros
    num_zeros = len(dishes_per_cuisine) - len(np.nonzero(dishes_per_cuisine)[0])
    if num_zeros > 0:
        print
        print("Removing %d cuisines because they contain zero dishes." % num_zeros)
        dishes_per_cuisine = dishes_per_cuisine[np.nonzero(dishes_per_cuisine)]

    # infer number of cuisines
    num_cuisines = len(dishes_per_cuisine)

    # ensure all cuisines have positive number of dishes
    for i in dishes_per_cuisine:
        assert i > 0, "Number of dishes must be positive for all cuisines."

    # ensure maximum number of cuisines is equal to number of letters
    assert num_cuisines <= len(LETTERS), \
        "A maximum of %d cuisines are allowed. Reduce length of input list." % len(LETTERS)

    # summary of inputs
    num_total_dishes = np.sum(dishes_per_cuisine)
    num_menus = np.prod(dishes_per_cuisine)
    print
    print("Generating menus ...")
    print
    print("Summary of inputs:")
    print("   Number of cuisines: " + str(num_cuisines))
    print("   Dishes per cuisine: " + str(dishes_per_cuisine))
    print("   Number of unique dishes: " + str(num_total_dishes))
    print("   Total number of menus: " + str(num_menus))

    if num_cuisines == 1:
        # if only one cuisine then each menu has exactly 1 dish
        cuisine_letter = 'A'
        menu_1cuisine = chararray_add(np.repeat(cuisine_letter, dishes_per_cuisine[0]),
                                      np.arange(1, dishes_per_cuisine[0] + 1).astype(str))

        # create a data frame for pretty printing
        result = pd.DataFrame(menu_1cuisine, columns=['Dishes', ])
        result.index = ['Menu' + str(i + 1) for i in range(result.shape[0])]

    else:
        # get cuisine letters from globally defined LETTERS variable
        cuisine_letters = LETTERS[0:num_cuisines]

        # create lists of available dishes
        available_dishes = dict()
        for i in range(num_cuisines):
            available_dishes[cuisine_letters[i]] = chararray_add(np.repeat(cuisine_letters[i], dishes_per_cuisine[i]),
                                                                 np.arange(1, dishes_per_cuisine[i] + 1).astype(str))

        # cross-product of dishes of first two cuisines
        menus = array_cross_product(available_dishes[cuisine_letters[0]], available_dishes[cuisine_letters[1]])

        # create menus by taking recursive cross-products for any further cuisines
        if num_cuisines > 2:
            for i in range(2, num_cuisines):
                menus = array_cross_product(menus, available_dishes[cuisine_letters[i]])

        # create a data frame for pretty printing
        result = pd.DataFrame(menus, columns=['Dishes', ])
        result.index = ['Menu' + str(i + 1) for i in range(result.shape[0])]

    print
    print("Resulting menus for %d cuisine(s), each with %s dishes" % (num_cuisines, dishes_per_cuisine))
    print
    print(result)
    print

    outfile = 'menus.txt'
    print("Writing menus to comma-separated file: %s" % outfile)
    result.to_csv(outfile, sep=',', index_label='MenuNumber')
    print('All done.')


if __name__ == '__main__':
    main(sys.argv)
