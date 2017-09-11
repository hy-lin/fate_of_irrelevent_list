loadData <- function(exp_number){
  data <- read.table(sprintf('Results/Data/Exp %d/irrelevent_list.dat', exp_number),
                     header = FALSE, 
                     fill = FALSE)
  names(data) <- c('ID',
                   'session',
                   'CSI',
                   'CLOperations',
                   'ProbeType',
                   'ProbeColor',
                   'ProbePosition',
                   'ItemIndex1', 'ItemPosition1',
                   'ItemIndex2', 'ItemPosition2',
                   'ItemIndex3', 'ItemPosition3',
                   'ItemIndex4', 'ItemPosition4',
                   'ItemIndex5', 'ItemPosition5',
                   'ItemIndex6', 'ItemPosition6',
                   'ProbeIndex', 'ProbePosition',
                   'Response', 'RT', 'OSCorrectness')
  data$ID <- factor(data$ID)
  data$session <- factor(data$session)
  data$CLOperations <- factor(data$CLOperations)
  data$ProbePosition <- factor(data$ProbePosition)
  data$ItemIndex1 <- factor(data$ItemIndex1)
  data$ItemIndex2 <- factor(data$ItemIndex2)
  data$ItemIndex3 <- factor(data$ItemIndex3)
  data$ItemIndex4 <- factor(data$ItemIndex4)
  data$ItemIndex5 <- factor(data$ItemIndex5)
  data$ItemIndex6 <- factor(data$ItemIndex6)
  data$ItemPosition1 <- factor(data$ItemPosition1)
  data$ItemPosition2 <- factor(data$ItemPosition2)
  data$ItemPosition3 <- factor(data$ItemPosition3)
  data$ItemPosition4 <- factor(data$ItemPosition4)
  data$ItemPosition5 <- factor(data$ItemPosition5)
  data$ItemPosition6 <- factor(data$ItemPosition6)
  data$ProbeIndex <- factor(data$ProbeIndex)
  data$ProbePosition <- factor(data$ProbePosition)
  data$Response <- factor(data$Response)
  
  return(data)
}

assignCorrectness <- function(data){
  for (i in 1:length(data$ID)){
    if (data$ProbeType[i] == 'positive'){
      if (data$Response[i] == 0){
        data$Correctness[i] = TRUE
      }else{
        data$Correctness[i] = FALSE
      }
    }else{
      if (data$Response[i] == 1){
        data$Correctness[i] = TRUE
      }else{
        data$Correctness[i] = FALSE
      }
    }
  }
  return(data)
}

exp1.data <- loadData(1)
exp1.data <- assignCorrectness(exp1.data)