#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math


class MainCLS:
    total_of_words = 0
    total_of_characters = 0
    current = 0
    user_longitude = 0
    user_use_letters = False
    user_use_lowercase = False
    user_use_uppercase = False
    user_use_numbers = False
    user_use_specials = False
    user_filename = ''
    list_string = ''

    def processWord(self, str):
        self.current = self.current + 1
        self.file_handler.write("%s\n" % str)
        sys.stdout.write("\r- Progress: %d/%d (%s)                " % (self.current, self.total_of_words, str))
        sys.stdout.flush()

    def loop(self, prefix, loops):
        if loops == 0:
            return

        last_list = []
        for id_letter in range(0, len(self.list_string)):
            final_str = prefix + self.list_string[id_letter]
            last_list.append(final_str)
            self.processWord(final_str)

        for id_array in range(0, len(last_list)):
            self.loop(last_list[id_array], loops - 1)

    def getInput(self, message, type_inp, default_value):
        inp = input(message)
        inp = inp.strip()

        if inp == '':
            inp = default_value

        if type_inp == 'int':
            try:
                val = int(inp)
                if val > -1:
                    return val
                else:
                    print
                    '- That\'s not an number. Try again.'
                    return self.getInput(message, type_inp, default_value)

            except ValueError:
                print
                '- That\'s not an number. Try again.'
                return self.getInput(message, type_inp, default_value)

        elif type_inp == 'bool':
            if inp.lower() == 'y':
                return True
            elif inp.lower() == 'n':
                return False
            else:
                print
                '- Please, respond with yes (y) or not (n). Try again.'
                return self.getInput(message, type_inp, default_value)

        elif type_inp == 'file':
            if os.path.isfile(inp):
                respond = self.getInput('- The file exists.You want to replace it? [y/N] : ', 'bool', 'n')
                if respond == False:
                    return self.getInput(message, type_inp, default_value)
                else:
                    return inp
            else:
                return inp

        else:
            return inp

    def printSummary(self):
        print
        '                                                       '
        print
        '  Summary                                              '
        print
        '  -----------------------------------------------------'
        print
        '- Max longitude of word                  : ' + '{0:,}'.format(self.user_max_longitude)
        print
        '- Total number of characters to use      : ' + '{0:,}'.format(len(self.list_string))
        print
        '- Total of words                         : ' + '{0:,}'.format(self.total_of_words)

        if self.user_use_letters == True:
            print
            '- Use letters                            : Yes'
            print
            '- Use lowercase letters                  : ' + ('Yes' if self.user_use_lowercase else 'No')
            print
            '- Use uppercase letters                  : ' + ('Yes' if self.user_use_uppercase else 'No')
        else:
            print
            '- Use letters                            : No'

        print
        '- Use numbers                            : ' + ('Yes' if self.user_use_numbers else 'No')
        print
        '- Use special chars                      : ' + ('Yes' if self.user_use_specials else 'No')
        if os.path.isfile(self.user_filename):
            print
            '- Filename of dictionary                 : ' + self.user_filename + ' (override)'
        else:
            print
            '- Filename of dictionary                 : ' + self.user_filename

        print
        '- File size estimated of dictionary      : ' + self.convertSize(self.total_of_characters)

        print
        '  -----------------------------------------------------'
        return self.getInput('- You want to proceed?        [Y/n]      : ', 'bool', 'y')

    def convertSize(self, size, precision=2):
        # size = size + 0.0
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
            suffixIndex += 1  # increment the index of the suffix
            size = size / 1024.0  # apply the division
        return ("%.*f%s" % (precision, size, suffixes[suffixIndex]))

    def __init__(self):

        print
        '- WHK Dictionary Maker 1.0, for pentesting purposes.';
        # self.user_min_longitude = self.getInput('- Enter min longitude of word [0]        : ', 'int',  '0')
        self.user_max_longitude = self.getInput('- Enter max longitude of word [4]        : ', 'int', '4')

        self.user_use_letters = self.getInput('- Use letters?                [Y/n]      : ', 'bool', 'y')
        if self.user_use_letters == True:
            self.user_use_lowercase = self.getInput('- Use lowercase?              [Y/n]      : ', 'bool', 'y')
            self.user_use_uppercase = self.getInput('- Use uppercase?              [y/N]      : ', 'bool', 'n')

        self.user_use_numbers = self.getInput('- Use numbers?                [Y/n]      : ', 'bool', 'y')
        self.user_use_specials = self.getInput('- Use special chars?          [y/N]      : ', 'bool', 'n')
        self.user_filename = self.getInput('- Filename of dictionary      [dict.txt] : ', 'file', 'dict.txt')

        self.list_string = ''

        if self.user_use_letters == True:

            if self.user_use_lowercase == True:
                self.list_string = self.list_string + 'abcdefghijklmnopqrstuvwxyz'

            if self.user_use_uppercase == True:
                self.list_string = self.list_string + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if self.user_use_numbers == True:
            self.list_string = self.list_string + '0123456789'

        if self.user_use_specials == True:
            self.list_string = self.list_string + '\\/\'"@#$%&/()=?¿!¡+-*_.:,;'

        self.total_of_words = 0
        self.total_of_characters = 0
        for n in range(0, self.user_max_longitude):
            total = (len(self.list_string) ** (n + 1))
            self.total_of_words = self.total_of_words + total
            # (word length * count words) + \n
            self.total_of_characters = self.total_of_characters + (total * (n + 1)) + total

        # Summary
        response = self.printSummary()
        if response == False:
            return

        # Load file
        if os.path.isfile(self.user_filename):
            os.remove(self.user_filename)
        self.file_handler = open(self.user_filename, 'w')

        # Execute all
        self.loop('', self.user_max_longitude)

        # End
        self.file_handler.close()
        print
        "\r                                                       \r- End!"


if __name__ == '__main__':
    mainCLS = MainCLS()
