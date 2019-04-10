from parse_table import table
import first_follow as ff
from lex_analyser import token as inp
from lex_analyser import pt

a = pt(['Matched', 'Stack', 'Input', 'Action'])

result = True

errmsg = ""

def parse(result):
    stack = []
    stack.append('$')
    stack.append('S')

    inp.append('$')

    next = inp.pop(0)
    matched = ['']

    global errmsg

    while stack and inp:
        inp_col = [next]
        top = stack.pop()

        if top in ff.non_term:
            entry = table[top].get(next, None)
            if entry == 'sync':
                result = False
                if top == 'S':
                    action = "ERROR : skip " + next

                    next = inp.pop(0)
                else:
                    action = "ERROR : pop " + top
                    top = stack.pop()

                errmsg += "\nError in parsing " + next

            if entry is None:
                result = False
                action = "ERROR : skip " + next
                errmsg += "\nError in parsing " + next
                next = inp.pop(0)
            else:
                action = str(top + " -> " + entry)
                if entry != 'epsilon':
                    stack.extend(entry.split()[::-1])

        else:  # top is a terminal
            if next == top:
                matched = [next]
                action = "Match " + next
                if inp:
                    next = inp.pop(0)

            else:
                result = False
                action = "ERROR : pop " + top
                errmsg += "\nError in parsing " + next
                #top = stack.pop()

        row = []

        row.extend(matched)
        matched = ['']
        row.append(" ".join(stack))  # in stack column
        row.append(next)  # in input column
        row.append("".join(action))  # in action column
        # print(row)
        a.add_row(row)  # adding row to the table


    return result,stack,inp


# main
errmsg = ""
result ,stack,inp = parse(result)

print("Moves made by the parser:")
print(a)


if result :
    if stack:
        print("The given string is accepted!!")
    else:
        print("The given string is not accepted..")
else:
    print("The given string is not accepted..")
    print(errmsg)