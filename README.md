Simple bayesian inference of the gender of a user based on its first name
=========================================================================

This lib implements a very simplistic model for infering the sex of a user 
based on its first name.

P(g | name) = P(name | g) P(g) / (P(name | male)P(male) + P(name | female)P(female))

The probabilities are estimated from a training list:

P(name | male) = (#(have name and is male)  + 1/2) / (#(male) + k/2)

where #(...) represents "number of ocurrences of ..." and k is the number 
of diferent names in our database

This formula is given by a Beta-Binomial model for gender given name.

