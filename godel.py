#
#   g o d e l . p y
#

    #########################################################
    #                                                       #
    #                   Global imports                      #
    #                                                       #
    #########################################################

from sys import stdout
from time import time

    #########################################################
    #                                                       #
    #                   Primes                              #
    #                                                       #
    #########################################################

# I may need a different strategy in the long run, but generating 
# the first thousand primes doesn't appear to take too long.
#
# For the future, see something like:
#   http://stackoverflow.com/questions/13326673/is-there-a-python-library-to-list-primes
#   http://stackoverflow.com/questions/567222/simple-prime-generator-in-python

"""
N=1000
N=65000 # Takes about 11 min on backie
N=94000 # Takes about 22 min on backie
N=100000 # Takes about 30 min on vector
def gen_primes():
    from numpy import mod
    start_time = time()
    primes = [2]
    next_number = 3
    while len(primes) < N:
        did_factor = False
        for p in primes:
            if (float(next_number) / float(p)) == (next_number / p):
                # It did factor, so increment next_number and to on
                did_factor = True
                break # quit testing
        if did_factor == False:
            # Add it to the primes table
            primes += [ next_number, ]
            if mod(len(primes), 5000) == 0:
                minutes = (time() - start_time) / 60.0
                print('  %.2f minutes:'%minutes),
                print('%s primes so far ...'%len(primes))
                stdout.flush()
        next_number += 1
    return(primes)
       
print('Generating %s primes ...'%N)
stdout.flush()
prime = gen_primes()
print('Done')
#print(prime)
"""

print('Reading primes from file ...'),
stdout.flush()
f = open('primes_100000.txt', 'r')
pstr = f.read()
exec('prime = ' + pstr)
print('Done')

    #########################################################
    #                                                       #
    #               Various Utility Functions               #
    #                                                       #
    #########################################################

#default_font_size = 4 # Seems good on Vector
default_font_size = 3 # Seems good on Backie

def Print(thing, font_size=None):
    if font_size == None: font_size = default_font_size
    from IPython.core.display import HTML
    from IPython.core.display import display
    display(HTML('<font size=%s>'%font_size+thing+'</font>'))

    #########################################################
    #                                                       #
    #               System Class and PM                     #
    #                                                       #
    #########################################################

class system:
    def __init__(self, name):
        self.name = name
        self.signs = []
   
    def add_sign(self, entry_value, display_value, godel_number):
        self.signs += [ (entry_value, display_value, godel_number), ] 

    def lookup_sign_number(self, snum):
        for sign in self.signs:
            if snum == sign[2]: return(sign)
        raise Exception(
            'Error trying to look up sign for invalid number %s'%snum)

    def lookup_sign_value(self, value):
        for sign in self.signs:
            if value == sign[0]: return(sign)
        raise Exception(
            'Error trying to look up sign for invalid value %s'%value)

    def show(self, fontsize=default_font_size):
        str = '<table>\n'
        str += '<tr>\n'
        str += '<td>Sign\n'
        str += '<td>Number\n'
        str += '<td>Enter\n'
        for sign in self.signs:
            str += '<tr><td>$%s$<td>$%s$'%(sign[1], sign[2])
            str += '<td>%s\n'%sign[0]
        str += '</table>'
        Print(str, fontsize)

#
# We'll predefine the system "PM" as given in Nagel and Newmann.
#

PM = system('PM')
PM.add_sign('~', r'\sim', 1)
PM.add_sign('V', r'\lor', 2)
PM.add_sign('>', r'\supset', 3)
PM.add_sign('E', r'\exists', 4)
PM.add_sign('=', '=', 5)
PM.add_sign('0', '0', 6)
PM.add_sign('s', 's', 7)
PM.add_sign('(', '(', 8)
PM.add_sign(')', ')', 9)
PM.add_sign(',', ',', 10)
PM.add_sign('+', '+', 11)
PM.add_sign('*', r'\times', 12)
PM.add_sign('x', 'x', 13)
PM.add_sign('y', 'y', 17)
PM.add_sign('z', 'z', 19)
PM.add_sign('p', 'p', 13**2)
PM.add_sign('q', 'q', 17**2)
PM.add_sign('r', 'r', 19**2)
PM.add_sign('P', 'P', 13**3)
PM.add_sign('Q', 'Q', 17**3)
PM.add_sign('R', 'R', 19**3)

    #########################################################
    #                                                       #
    #               Sentence Class                          #
    #                                                       #
    #########################################################

class sentence:
    def __init__(self, system, string):
        self.system = system # Save the system we're using
        # We examine each character of the string entered
        n = 0 # Start with the 0th char in the string
        self.S = [] # S will be the "encoded" sentence
        while n < len(string):
            c = string[n]
            # If it's a non-zero digit, then we deal with an integer.
            # Note that get_integer will reposition n.
            if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                n, number = self.get_number(n, string)
                self.S += [ (-1, number), ]
            # Otherwise, we just add the sign number to the encoded list
            else:
                sign, disp, num = self.system.lookup_sign_value(c)
                self.S += [ (num,) ]
            n += 1 

    def get_number(self, n, string):
        nstr = ''
        while(
            n < len(string) and
            string[n] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            nstr += string[n]
            n += 1
        return( n-1, int(nstr) )

    #
    # Different formats in which we can view the sentence
    #

    # Look at the raw encoded sentence
    def as_raw(self): return(self.S)

    # View is as a sentence. Potentially change numbers to 's's.
    def as_sentence(self, force_s=False):
        string = ''
        for tuple in self.S:

            if tuple[0] > 0: 
                # It's the number of a sign. Look it up.
                sign, disp, num = self.system.lookup_sign_number(tuple[0])
                string += disp + ' '

            elif tuple[0] == -1:
                # -1 indicates a (regular) number
                if force_s:
                    # We're assuming 's' and '0'
                    for n in range(tuple[1]): string += 's'
                    string += '0'
                else:
                    string += str(tuple[1]) + ' '

            elif tuple[0] == -2:
                # -2 indicates a goedel number
                string += r'\hat{g} '

            else:
                print('tuple[0] = %s'%tuple[0])
                raise Exception('Error in string encoding')
        return(string)

    # As a goedel number, displayed as factors
    def as_g_factors(self, times=True):
        g_str = ''
        saw_gnum = False
        prime_index = 0
        for tuple in self.S:
            snum = tuple[0]
            # If the sign number is greater than 0, then we use it as
            # the exponent of the next prime.
            if tuple[0] > 0: 
                if times and g_str != '': g_str += r'\times '
                if saw_gnum:
                    g_str += 'P_{g+%s}^{%s}'%(prime_index+2, tuple[0])
                else:
                    g_str += '%s^{%s}'%(prime[prime_index], tuple[0])
                prime_index += 1
            # If it's -1 then we have an integer. This needs to be translated
            # into some number of 's' sign numbers
            elif snum == -1:
                if times and g_str != '': g_str += r'\times '
                # We are ASSUMING that every 'system' has a successor
                # function called 's' and also has a '0'
                sign, disp, succ_num = self.system.lookup_sign_value('s')
                for n in range(tuple[1]):
                    if saw_gnum:
                        g_str += 'P_{g+%s}^{%s}'%(prime_index+2, succ_num)
                    else:
                        g_str += '%s^{%s}'%(prime[prime_index], succ_num) 
                    prime_index += 1
                    if times and n < tuple[1]-1: g_str += r'\times '
                if times and g_str != '': g_str += r'\times '
                sign, disp, zero_num = self.system.lookup_sign_value('0')
                g_str += '%s^{%s}'%(prime[prime_index], zero_num)
            elif tuple[0] == -2:
                # -2 indicates a goedel number
                sign, disp, succ_num = self.system.lookup_sign_value('s')
                sign, disp, zero_num = self.system.lookup_sign_value('0')
                if times and g_str != '': g_str += r'\times '
                g_str += r'%s^{%s} '%(prime[prime_index], succ_num)
                if times : g_str += r'\times '
                g_str += ' ... '
                if times : g_str += r'\times '
                g_str += 'P_{g+%s}^{%s} '%(prime_index, succ_num)
                if times : g_str += r'\times '
                g_str += 'P_{g+%s}^{%s} '%(prime_index+1, zero_num)
                saw_gnum = True
            else:
                print('tuple[0] = %s'%tuple[0])
                raise Exception('Error in string encoding')
        return(g_str)

    # As a goedel number, as an actual python integer
    # (which will automatically be arbitrary precision, if necessary)
    def as_g_number(self):
        sign, disp, zero_num = self.system.lookup_sign_value('0')
        sign, disp, succ_num = self.system.lookup_sign_value('s')
        g_num = 1
        prime_index = 0
        for tuple in self.S:
            snum = tuple[0]
            # If the sign number is greater than 0, then we use it as
            # the exponent of the next prime.
            if tuple[0] > 0: 
                g_num *= prime[prime_index]**snum
                prime_index += 1
            # If it's -1 then we have an integer. This needs to be translated
            # into some number of 's' sign numbers to use as exponents
            elif snum == -1:
                # We are ASSUMING that every 'system' has a successor
                # function called 's' and also has a '0'
                for n in range(tuple[1]):
                    g_num *= prime[prime_index]**succ_num
                    prime_index += 1
                g_num *= prime[prime_index]**zero_num
            elif tuple[0] == -2:
                # -2 indicates a goedel number
                    print('Warning: Encountered an embedded Goedel number:')
                    embedded_g = tuple[1].as_g_number()
                    Print('$%s$'%embedded_g)
                    print('This could get ugly ...')
                    stdout.flush()
                    start_time = time()
                    tt = 0
                    while embedded_g > 0:
                        g_num *= prime[prime_index]**succ_num
                        prime_index += 1
                        embedded_g -= 1
                        if time() - start_time > 60:
                            start_time = time()
                            tt += 1
                            print('  %s min: countdown = %s'%(tt, embedded_g))
                            stdout.flush()
                    stdout.flush()
                    g_num *= prime[prime_index]**zero_num
                    print('Expansion done. "0" prime was %s.'
                        %prime[prime_index])
                    prime_index += 1
            else:
                print('tuple[0] = %s'%tuple[0])
                raise Exception('Error in string encoding')
        return(g_num)
        
# Take the given sentence and replace all occurrences of the specified 
# sign with the goedel number g. Note that g is actually stored as a
# sentence.
#
def sub(system, old_sentence, sign, g):
    # Look up the encoding number for the sign
    sval, descr, snum = system.lookup_sign_value(sign)
    # Now we simply replace any tuple containing that sign with a
    # "goedel number tuple" whose 2nd value is (the sentence) g
    new_sentence = sentence(PM, '')
    for t in old_sentence.S:
        if t[0] == snum: new_sentence.S += [ (-2, g), ]
        else: new_sentence.S += [ t, ]
    return(new_sentence)

