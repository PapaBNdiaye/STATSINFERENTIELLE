# Chargement des packages necessaires
library(dplyr)
library(gt)
library(rstatix)

#' Fonction pour obtenir le V de Cramer pour toutes les paires de variables ainsi que les p-values
#'
#' @param data Un dataframe contenant les variables catégorielles à analyser.
#' 
#' @return Un dataframe contenant les paires de variables, leur p-value de chi2 et leur V de Cramer correspondant.
#'
#' @note Le V de Cramer est une mesure de l'association entre deux variables catégorielles.
#' NB : les variables doivent être en factor.

Table.Cramer.chi2 <- function(data) {
  vars <- names(data)
  results <- data.frame()
  for(i in 1:(length(vars)-1)) {
    for(j in (i+1):length(vars)) {
      test <- chisq.test(as.factor(data[[vars[i]]]), as.factor(data[[vars[j]]]))
      v <- cramer_v(as.factor(data[[vars[i]]]), as.factor(data[[vars[j]]]))
      results <- rbind(results, 
                       data.frame(var1 = vars[i], 
                                  var2 = vars[j], 
                                  v = v,
                                  pvalue_chi2 = test$p.value))
    }
  }
  return(results)
}



######################################
# Exemple sur le jeu de données mtcars pour fixer les idées 

df <- mtcars %>% 
  mutate(am = factor(am), cyl = factor(cyl))%>%
  select(cyl, vs, am)

results <- Table.Cramer.chi2(df)
print(results)
