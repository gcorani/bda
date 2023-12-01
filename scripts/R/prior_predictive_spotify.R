#prior predictive check for the spotify example
a <- rnorm(5000, mean = 50, sd = 10)

xi <- 36 

vec <- vector(length = length(a))
for (i in 1:length(vec)){
  sigma <- abs(rnorm(1, mean = 0, sd=xi))
  vec[i] <- rnorm(1, mean = a[i], sd = sigma)
}
hist(vec)
