#
# formal_systems.py
#

    #########################################################
    #                                                       #
    #               Utility Functions                       #
    #                                                       #
    #########################################################

#default_font_size = 4 # Seems good on Vector
default_font_size = 3 # Seems good on Backie
default_sleep_time = .1

def Print(thing, font_size=None, sleep_time=None):
    from sys import stdout
    from time import sleep
    if font_size == None: font_size = default_font_size
    if sleep_time == None: sleep_time = default_sleep_time
    from IPython.core.display import HTML
    from IPython.core.display import display
    display(HTML('<font size=%s>'%font_size+thing+'</font>'))
    stdout.flush(); sleep(sleep_time)

    #########################################################
    #                                                       #
    #               Formal Systems Classes                  #
    #                                                       #
    #########################################################

# A formal_system needs to be initialized with
#
#   (1) a list called "axioms"
#   (2) a list called "rules"

class formal_system:

    # "Display form" of a string
    def dsp(self, entry_str):
        disp_str = ''
        for char in entry_str:
            if char == ' ': continue # Strip out spaces
            try:
                sign, disp, num = self.lookup_sign_value(char)
            except Exception:
                # If we can't look it up, just use the original character
                disp = char
            disp_str += disp + ' '
        return(disp_str)

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

    def show_axioms(self):
        n = 0
        for a in self.axioms:
            n += 1
            Print('$%s.\; %s$' %( n, self.dsp(a) ))

    def show_theorems(self, first=1, last=10):
        nt = len(self.theorems)
        if last > nt: last = nt
        for n in range(first, last+1):
            T = self.theorems[n-1]
            Print('$%s.\; %s$' %(n, self.dsp(T)))
        if last < nt:
            Print('There are more theorems. Use show_theorems(m, n)')

    def count(self, char, string):
        n = 0
        for c in string:
            if c == char: n += 1
        return(n)

    def isTheorem(self, T):
        for theorem in self.theorems:
            if T == theorem: return(True)
        return(False)

    # Enumerate theorems. One "cycle" means that you apply every
    # rules to every existing theorem. So the first cycle you would
    # apply each rule to each axiom, and store every new theorem.
    # The next cycle, you would apply every rule to each of the newly
    # produces theorems, and so on. This continues until either the
    # specified number of cycles has been done, or the time limit
    # is reached. If num_cycles is 0, then you just run until the
    # time limit is reached.

    # Enumerate does not reset the theorem list. It will pick up
    # where it left off, if you start it again.

    def enumerate(self, num_cycles=0, time_limit=1, verbose=False):
        from time import time
        start_time = time()
        elapsed_time = 0
        cycle = 0
        n_new_t = 0
        while elapsed_time <= time_limit:
            # Use every rule on every theorem
            cycle += 1
            if num_cycles != 0 and cycle > num_cycles: break
            if verbose: Print('[Cycle %s]' %cycle)
            first_th = self.last_theorem_done
            last_th = len(self.theorems)-1
            #print('This cycle will do theorems %s to %s'%(first_th,last_th))
            for th_num in range(first_th, last_th+1):
                T = self.theorems[th_num]
                if verbose: Print('[Theorem %s]' %th_num)
                for R in self.rules:
                    new = R(T)
                    # Unfortunately, as far as I can see, we are going to
                    # have to search through all the existing theorems to
                    # see if we have a new one. Ultimately, if we really
                    # want to have a big list, I guess we've want to keep
                    # it sorted and do a binary search.
                    if self.isTheorem(new)==False:
                        if verbose: Print(r'[New Theorem: %s]'%new)
                        self.theorems += [ new, ]
                        n_new_t += 1
                self.last_theorem_done += 1
                elapsed_time = time() - start_time
                if elapsed_time >= time_limit: break
        ttime = time() - start_time
        Print('[Generated %s new theorems in %.2f seconds]'%(n_new_t,ttime))

    # Try to "prove" (or derive) a theorem (by hand)
    def prove(self):
        inp = raw_input('Enter a theorem or number:')
        t_num = -1
        try: t_num = int(inp) - 1
        except Exception: pass
        if t_num >= 0 and t_num < len(self.theorems):
            T = self.theorems[t_num]
        else:
            if self.isTheorem(inp):
                T = inp
            else:
                Print('$%s$ is not a theorem.'%self.dsp(inp))
                return

        # At this point we have a good starting theorem
        Print('$%s$' %self.dsp(T)) 
        while(True):
            rule_num = raw_input('Rule:')
            if rule_num == 'q': break
            try: rule_num = int(rule_num) - 1
            except Exception:
                Print('q to quit')
                continue
            if rule_num < 0 or rule_num >= len(self.rules):
                Print('Rule number must be between %s and %s'
                    %(1, len(self.rules)))
                continue
            # At this point we have a rule to apply
            msg = self.dsp(T)
            new_t = self.rules[rule_num](T)
            if new_t != T:
                # Add the new theorem
                T = new_t
                self.theorems += [ T, ]
                # Display the change
                msg += r'\rightarrow ' + self.dsp(T)
            Print('$%s$'%(msg))

#
# The MU System from GEB
#

class MU(formal_system):

    def __init__(self, verbose=False):
        self.name = 'MIU'
        self.V = verbose

        self.signs = []
        self.add_sign('M', r'\mathrm{M}', 0)
        self.add_sign('I', r'\mathrm{I}', 0)
        self.add_sign('U', r'\mathrm{U}', 0)

        self.axioms = [ 'MI', ]
        self.rules = [ self.RI, self.RII, self.RIII, self.RIII, self.RIV ]
        self.theorems = list(self.axioms) # All axioms are theorms
        self.last_theorem_done = 0 # For enumerate

    def RI(self, old):
        if old[len(old)-1] == 'I': new = old+'U'
        else: new = old
        if self.V: Print(r'Rule I: %s $\rightarrow$ %s'%(old, new))
        return(new)

    def RII(self, old):
        if len(old) > 1 and old[0] == 'M': new = old+old[1:]
        else: new = old
        if self.V: Print(r'Rule II: %s $\rightarrow$ %s'%(old, new))
        return(new)

    # Rule III (page 34) says that if III occurs in a string you can
    # replace it with U. So, what I'm doing here is NOT actually trying
    # all the possibilities if the old string has more than one III.
    # I'm assuming right now that there is only a single occurance. I'll
    # enhance that later.
    def RIII(self, old):
        i = -1
        try: i = old.index('III')
        except ValueError: new = old
        if i > -1: new = old[:i] + 'U' + old[i+3:] 
        if self.V: Print(r'Rule III: %s $\rightarrow$ %s'%(old, new))
        return(new)

    # Rule IV (pate 35) just like in Rule III I'm ignoring the possibility
    # that UU occurs more than once, and I might get a diffferent resulte
    # by dropping a different one.
    def RIV(self, old):
        i = -1
        try: i = old.index('UU')
        except ValueError: new = old
        if i > -1: new = old[:i] + old[i+2:] 
        if self.V: Print(r'Rule IV: %s $\rightarrow$ %s'%(old, new))
        return(new)

#
# The TNT system from GEB
#

class TNT(formal_system):

    def __init__(self, verbose=False):
        self.name = 'TNT'
        self.V = verbose

        # GEB page 268
        self.signs = []
        self.add_sign('0', '0', 666)
        self.add_sign('S', r'\mathrm{S}', 123)
        self.add_sign('=', '=', 111)
        self.add_sign('+', '+', 112)
        self.add_sign('.', r'\cdot', 236)
        self.add_sign('(', '(', 362)
        self.add_sign(')', ')', 323)
        self.add_sign('<', r'\lt', 212)
        self.add_sign('>', r'\gt', 213)
        self.add_sign('[', '[', 312)
        self.add_sign(']', ']', 313)
        self.add_sign('a', 'a', 262)
        self.add_sign("'", "'", 163)
        self.add_sign('^', r'\land', 161)
        self.add_sign('v', r'\lor', 616)
        self.add_sign('}', r'\supset', 633)
        self.add_sign('~', r'\sim', 223)
        self.add_sign('E', r'\exists', 333)
        self.add_sign('A', r'\forall', 626)
        self.add_sign(':', ':', 636)
        self.add_sign(';', ';', 611) # What he calls 'punc.'

        self.axioms = [
            "Aa:~Sa=0",
            "Aa:(a+0)=a",
            "Aa:Aa':(a+Sa')=S(a+a')",
            "Aa:(a.0)=0",
            "Aa:Aa':(a.Sa')=((a.a')+a)"]
        self.theorems = list(self.axioms) # All axioms are theorms
        self.last_theorem_done = 0 # For enumerate

        self.rules = [ ]

