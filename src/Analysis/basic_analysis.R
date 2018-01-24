library(ggplot2)
library(BayesFactor)

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

filterOutlier <- function(data){
  for (i in 1:length(data$ID)){
    #if (data$RT[i] > 5000){
    #  data$Correctness[i] = NaN
    #  data$RT[i] = NaN
    #}
    
    if (!is.nan(data$Correctness[i]) && data$Correctness[i] == FALSE){
      data$RT[i] = NaN
    }
    
    #if (data$OSCorrectness[i] / data$CLOperations[i] < 0.6){
    #  data$Correctness[i] = NaN
    #  data$RT[i] = NaN
    #}
  }
  return(data)
}

exp1.data <- loadData(1)
exp1.data <- assignCorrectness(exp1.data)

exp1.data <- filterOutlier(exp1.data)


data <- data.frame(aggregate(list(exp1.data$Correctness, exp1.data$RT), list(exp1.data$ID, exp1.data$CLOperations, exp1.data$ProbeType), mean, na.rm = TRUE))
names(data) <- c('ID', 'CLOperations', 'ProbeType', 'PC', 'RT')
data$CLOperations <- factor(data$CLOperations)

tmp_data <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$CLOperations), mean))
tmp_data_sd <- data.frame(aggregate(list(data$PC, data$RT), list(data$ProbeType, data$CLOperations), sd))
tmp_data[, 5] <- tmp_data_sd[, 3] / sqrt(10)
tmp_data[, 6] <- tmp_data_sd[, 4] / sqrt(10)
names(tmp_data) <- c('ProbeType', 'CLOperations', 'PC', 'RT', 'PC_SE', 'RT_SE')
pd <- position_dodge(.1)
ggplot(data=tmp_data) + aes(x=CLOperations, y = PC, linetype = ProbeType, group = ProbeType) + 
  geom_line(position = pd) + 
  geom_errorbar(aes(ymin=PC-PC_SE, ymax=PC+PC_SE), width=.1, position = pd) + 
  geom_point(position = pd)

cl.probetype <- anovaBF(PC ~ ProbeType * CLOperations + ID, data=data[data$ProbeType != 'positive',], whichRandom = 'ID')
cl.probetype
cl.probetype[3] / cl.probetype[4]

cl.probetype <- anovaBF(PC ~ ProbeType * CLOperations + ID, data=data, whichRandom = 'ID')
cl.probetype
cl.probetype[3] / cl.probetype[4]

ggplot(data=tmp_data) + aes(x=CLOperations, y = RT, linetype = ProbeType, group = ProbeType) + 
  geom_line(position = pd) + 
  geom_errorbar(aes(ymin=RT-RT_SE, ymax=RT+RT_SE), width=.1, position = pd) + 
  geom_point(position = pd)

cl.probetype <- anovaBF(RT ~ ProbeType * CLOperations + ID, data=data[data$ProbeType != 'positive',], whichRandom = 'ID')
cl.probetype
cl.probetype[3] / cl.probetype[4]


cl.probetype <- anovaBF(RT ~ ProbeType * CLOperations + ID, data=data, whichRandom = 'ID')
cl.probetype
cl.probetype[3] / cl.probetype[4]
