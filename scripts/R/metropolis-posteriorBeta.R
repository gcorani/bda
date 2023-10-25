metropolis  <- function() {
  library(fpp2)
  set.seed(42)
  
  theta <- vector(length = 10000)
  proposal_sd <- c(0.01, 0.1, 0.18, 0.3)
  df <- data.frame(proposal_sd)
  df$accepted <- 0
  df$post_mean <- 0
  df$theta_star <- 0
  
  #prior
  a <- 5
  b <- 5
  y <- 15
  n <- 20
  actual_theta_post <- (a + y) / (a +b + n)
  
  
  
  for (sd_idx in 1:length(proposal_sd)){
    #theta0
    theta[1] <- 0.5
    accepted <- 0
    current_sd <- proposal_sd[sd_idx]
    df$proposal_sd[sd_idx] <- current_sd
    df$theta_star <- actual_theta_post
    print(current_sd)
    for (i in (2:length(theta))){
      
      
      proposal <- theta[i-1] + rnorm(n=1, sd=current_sd)
      proposal <- min (1, proposal)
      proposal <- max (0, proposal)
      
      post_current  <- dbinom(y, n, prob = theta[i-1]) * dbeta(theta[i-1], a, b)
      post_proposal <- dbinom(y, n, prob = proposal) * dbeta(proposal, a, b)
      prob_change   <- min(1,  post_proposal/post_current)
      if (runif(1) < prob_change){
        theta[i] = proposal
        accepted <- accepted + 1
      }
      else {
        theta[i] = theta[i-1]
      }
    }
    df$accepted[sd_idx] <- accepted / length(theta)
    df$post_mean[sd_idx] <- mean(theta)
    df$corr[sd_idx] <- cor(theta[1:9999], theta[2:10000])
    p <- autoplot(ts(theta)) + ggtitle(paste("sd = "), as.character(current_sd))
    ggsave(p, filename = paste("sd", as.character(current_sd),".png"))
  }
  return(df)
}
