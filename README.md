One quality model which is a transformer. Given an input sequence and a previous token sequence, use a linear layer at the end to assign the quality of picking any particular card

We can represent the available pieces as either a bag of words vector ([1, 0, 0, 2, 0, 1])
or a token sequence ([ZERO, ONE, TWO, TWO, *, /, +])
We can use a transformer which does not add positional encoding

I prefer the token sequence


0 - 10 | 11
+ - * / | 4
MASK | 1

hand = 4 numbers + 3 operators
