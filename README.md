# Automaton checker

### Usage:
1. modify `input.txt` and `config.json`
2. run `tester.py` from terminal

### Config:

You can change the input file (local dir)

```js
"file": "input.txt"
```

You can change if you want to see advanced logs or not

```js
"debug": true,
```

You can change what type of checker/emulator you want to run

```js
"type": "NFA"
```
or
```js
"type": "DFA"
```
or
```js
"type": "CFG"
```
or
```js
"type": "PDA"
```

### Examples of inputs:

DFA that will check if a string ends with b and contains at least one a

```py
Input:
    a
    a
    a
    a
    b
    a
    a
    b
    a
    b
    b
    b
End

Sigma:
    a
    b
End

States:
    q1 # valid
    q2 # se termina cu a
End

# va da check la orice string format din a si b care se termina in b
Transitions:
    q1, a, q2 # there s no need to add a "q2, a, q2" because the emulator ignores nonexistent transitions
    q2, b, q1
End

Initial:
    q1
End

Final:
    q1
End
```

NFA that will check if a string is made
- of "a" repeated by a number that is a multiple of 2
  
or

- of "b" repeated by a number that is a multiple of 3
Use * for epsilon.

```py
Input:
    a
    a
    a
    a
End

Sigma:
    a
    b
End

States:
    q1
    q2
    q3
    q4
    q5
    q6
    q7
    q8
End

# va verifica daca inputul 
# este un text format din a care se repeta de un nr div cu 2
# sau daca e format din b care se repeta de un nr div cu 3
# * = epsilon
Transitions:
    q1, *, q2 # primul ciclu
    q2, a, q3
    q3, a, q4
    q4, a, q3 # mod
    q1, *, q5 # al doilea ciclu
    q5, b, q6
    q6, b, q7
    q7, b, q8
    q8, b, q6 # mod
End

Initial:
    q1
End

Final:
    q4
    q8
End
```

CFG that generates strings such as `a cat danced with the cat` or `John sang to the bird`, etc...

Use | for separating multiple choices.

```py
Variables:
    S
    NP
    VP
    PP
    Det
    N
    PN
    V
    P
End

Sigma:
    the
    a
    dog
    cat
    bird
    unicorn
    John
    Mary
    Bob
    Alice
    chased
    petted
    sang
    to
    danced
    with
    on
    under
End

Rules:
    S -> NP VP
    NP -> Det N | PN
    VP -> V NP | V NP PP
    PP -> P NP
    Det -> the | a
    N -> dog | cat | bird | unicorn
    PN -> John | Mary | Bob | Alice
    V -> chased | petted | sang to | danced with
    P -> with | on | under
End

Input:
    S
End
```

PDA that checks if a string has a valid parenthesis pattern such as ()()()(()(()(()(())()))())

Use "epsilon" for epsilons.

Transitions commands: "push X", "pop", "check X", (where X is your symbol)

```py
Input:
    (
        (
        )
        (
        )
    )
End

Sigma:
    (
    )
End

States:
    Q # q e ok 
    P # p - processing
End

Transitions:
    Q, (, epsilon, push A, P # paranteza deschisa prima
    P, (, epsilon, push A, P # o paranteza deschisa in timpu procesarii
    P, ), A, pop, P # se taie de pe stiva
    P, epsilon, $, check $, Q # finalul cand stacku e gol
End

Initial:
    Q
End

Final:
    Q
End

StackSymbols:
    A
    $
End

StackInitial:
    $
End
```