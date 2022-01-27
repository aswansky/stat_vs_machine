* Encoding: UTF-8.
DISCRIMINANT 
  /GROUPS=death(0 1) 
  /VARIABLES=sex patient_type pneumonia age  diabetes copd asthma inmsupr hypertension 
    other_disease cardiovascular obesity renal_chronic tobacco contact_other_covid 
  /ANALYSIS ALL 
  /METHOD=WILKS 
  /FIN=3.84 
  /FOUT=2.71 
  /SAVE=CLASS 
  /PRIORS SIZE 
  /HISTORY 
  /STATISTICS=TABLE 
  /CLASSIFY=NONMISSING SEPARATE.

DATASET ACTIVATE DataSet1.
DISCRIMINANT
  /GROUPS=patient_type(1 2)
  /VARIABLES=pneumonia
  /ANALYSIS ALL
  /SAVE=CLASS 
  /PRIORS EQUAL 
  /CLASSIFY=NONMISSING POOLED.

LOGISTIC REGRESSION VARIABLES death 
  /METHOD=FSTEP(COND) pneumonia age diabetes copd asthma inmsupr hypertension other_disease 
    cardiovascular obesity renal_chronic tobacco contact_other_covid covid_res 
  /CONTRAST (pneumonia)=Indicator 
  /CONTRAST (diabetes)=Indicator 
  /CONTRAST (copd)=Indicator 
  /CONTRAST (asthma)=Indicator 
  /CONTRAST (inmsupr)=Indicator 
  /CONTRAST (hypertension)=Indicator 
  /CONTRAST (other_disease)=Indicator 
  /CONTRAST (cardiovascular)=Indicator 
  /CONTRAST (obesity)=Indicator 
  /CONTRAST (renal_chronic)=Indicator 
  /CONTRAST (tobacco)=Indicator 
  /CONTRAST (contact_other_covid)=Indicator 
  /CONTRAST (covid_res)=Indicator 
  /CLASSPLOT 
  /PRINT=SUMMARY 
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.1).
