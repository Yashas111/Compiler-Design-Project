import first_follow as ff
from lex_analyser import pt
#from prettytable import PrettyTable

def ll_table():

    table = {}
    prod = ff.prod
    foll = ff.follows


    for n_term in prod:
        table[n_term] = {}      #n_term -> rule
        for rule in prod[n_term] :
            f = ff.first_of_string(rule)
            for term in f:
                if term in table[n_term] :
                    print("Not an LL(1) Grammar!!")
                    exit(0)

                if rule != "epsilon" and term != "epsilon":
                    #print(n_term,term,rule)
                    table[n_term][term] = rule


    for n_term in foll:
        if "epsilon" in prod[n_term]:
            for term in foll[n_term]:
               # print(table[n_term][term])
               if not table[n_term].get(term, None):
                   table[n_term][term] = "epsilon"

    for n_term in foll:
        for term in foll[n_term]:
            entry = table[n_term].get(term,None)
            if entry is None:
                table[n_term][term]='sync'


    return table

#print(ff.first)
#print(ff.prod)

'''
foreach(A -> α in the grammar):
  write A -> α in T[A,b], ∀  b ∈ first(α);
  if ( ℇ ∈ first(α) ):
     write A -> α in T[A,x], ∀ x ∈ follow(A);
'''

table = ll_table()


cols = ['Non-Term']
term = ff.term
term.remove('epsilon')
term.append('$')
cols.extend(term)
a = pt(cols)

for i in table:
    row = [i]
    for t in term:

        if t not in table[i]:
            row.append('')
        else:
            row.append(str(table[i][t]))

    a.add_row(row)

print("Parse Table :")
print(a)


