libs.required <-c("tidyverse", "R0", "ggplot2", "dplyr", "maps", "ggmap", "mongolite", "lubridate", "gridExtra", "stringr")
# install.packages(libs.required)
lapply(libs.required, library, character.only = TRUE)

df<-read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
df <-dplyr::select(df, -iso3, -iso2, -FIPS, -UID, -code3, -Admin2, -Country_Region, -Lat, -Long_, -Combined_Key)


# Fetch Collections
countryDemographics = mongo(collection = "country_demographics", db="covid19", url = "mongodb://104.251.210.60:25043", )
countyDemographics = mongo(collection = "county_demographics", db="covid19", url = "mongodb://104.251.210.60:25043", )
statistics = mongo(collection = "statistics", db="covid19", url = "mongodb://104.251.210.60:25043", )

# Get a list of countries
countries = countryDemographics$distinct("country")

# Pre defined function
mGT<-generation.time("gamma", c(3, 1.5))

getR0Country <- function(countryDf, population){
  # cityDf <- colSums(dplyr::select(dplyr::filter(df, Province_State==city), -Province_State))  
  countryDf = countryDf[countryDf>0]
  estR0<-estimate.R(as.vector(t(countryDf)), mGT, begin=1, end=length(countryDf)-1, methods=c("EG"),
                    pop.size=population, nsim=100)
  return (estR0$estimates$EG$R)
}

getCountryPopulation <- function(countryName){
  pop <- t(countryDemographics$find(str_glue('{{"country":"{countryName}"}}'))['country_population'])[1]
  return (pop)
}

getCountyPopulation<- function(countyName, stateName){
  pop <- t(countyDemographics$find(str_glue('{{"county":"{countyName}", "state":"{stateName}"}'))['jhu_county_population'])[1]
  return (pop)
}

getCountryConfirmedStats<- function(countryName){
  qur <- paste('[
  {
    "$addFields": {
      "date": {
        "$toDate": "$date"
      }
    }
  },
  {
    "$match": {
      "country": "',countryName,'"
    }
  },
  {
    "$group": {
      "_id": "$date",
      "confirmed": {
        "$sum": "$confirmed"
      }
    }
  },
  {
    "$sort": {
      "_id": 1
    }
  }
]', sep="")
  stats <- statistics$aggregate(qur)
  return (stats)
}


pb = txtProgressBar(min = 0, max = length(countries), initial = 0) 
c=0
for(country in countries){
  setTxtProgressBar(pb,c)
  countryStats = getCountryConfirmedStats(country)[2]
  r0 = getR0Country(countryStats, getCountryPopulation(country))
  # print(paste(country,':', r0))
  countryDemographics$update(str_glue('{{"country":"{country}"}}'),str_glue('{{"$set":{{"country_r0":{r0}}}}}'))
  c=c+1
  }
