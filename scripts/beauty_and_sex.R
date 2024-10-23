# A study of American adolescents whose attractiveness on a five-point scale was assessed.
# Years later, many of these survey respondents had children.
# The original analysis compared the sex ratio of children of the “very attractive” parents to all other.
# For example, several years ago a researcher analyzed data from a survey of 3000 Americans
# 56% of the children of parents in the highest attractiveness category were girls, 
# compared to 48% of the children of parents in the other categories.
# Out of the 3000, 10% were labelled in the highest attractiveness category.
# Is the difference significant?

#frequentist test
n1 <- 300
n2 <- 2700
p1 <- .56
p2 <- .48
pbar <- (p1 * n1 + p2 * n2) / (n1 + n2)
sd_err <- sqrt( pbar * ( 1 - pbar) * (1/n1 + 1/n2) )
z <- (p1 - p2) / sd_err # 2.6, significant

#Bayesian test

# The variation in the human sex ratio occurs in a very narrow range. 
# For example, a recent count in the United States reported 48.7% girls among whites 
# and 49.2% among blacks.
# In the world, it varies between 46% and 50%.
# Similar differences of half of a percentage point or less have been found when comparing
# based on factors such as birth order, maternal age, or season of birth. 
# Given that attractiveness is itself only subjectively measured, 
#we would find it hard to believe that any difference between more and less attractive 
#parents could be as large as 0.5%.

#tune the beta
a = 48
get_b <- function (a){
  return ( a * 52/48)
}

quantile(rbeta(n=10000, a, get_b(a)), c(0.025,0.975)) # 0.38 - 0.58 

a = 480
quantile(rbeta(n=10000, a, get_b(a)), c(0.025,0.975)) # 0.45 - 0.51
         
a = 800
b = get_b(a)
quantile(rbeta(n=10000, a, b), c(0.025,0.975)) # 0.455 - 0.505
#prior strenght: 800 + 866 = 1666, comparable to the size of the study

#posterior
post_1 <- c(a + p1 * n1, b + (1 - p1) * n1) 
post_2 <- c(a + p2 * n2, b + (1 - p2) * n2) 

CI_group1 <- qbeta ( c(0.025,0.975), post_1[1], post_1[2])
CI_group2 <- qbeta ( c(0.025,0.975), post_2[1], post_2[2])

diff <- rbeta(n=10000, post_1[1], post_1[2]) - 
    rbeta(n=10000, post_2[1], post_2[2]) 
#CI contains the 0 and hence difference  is not significant
CI_diff <- quantile(diff, c(0.025,0.975))
