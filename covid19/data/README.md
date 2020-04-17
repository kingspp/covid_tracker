#List of Data Sources


# Data Operations

Source Name: Religious Composition by Country 2020

1. Filter on Year=2020 and extract required columns - Region,Country,Christians,Muslims,Unaffiliated,Hindus,Buddhists,Folk Religions,Other Religions,Jews,All Religions
2. Replace \s\s+ with  ""
3. Rename Continents :

    | Previous  | After  |
    |---|---|
    | Asia-Pacific | Asia  |
    | Asia-Pacific (Australia)  | Australia  |
    | Latin America-Caribbean | South America|
    | Middle East-North Africa | Africa |
    | Sub-Saharan Africa | Africa |

4. Rename Countries (In accordance with JHU) :

    | Previous  | After  |
    |---|---|
    | United States | US  |
    | Taiwan  | Taiwan*  |
    | Republic of Macedonia | North Macedonia|
    | South Korea | "Korea, South" |
    | Republic of the Congo | Congo (Brazzaville) |
    | Democratic Republic of the Congo | Congo (Kinshasa) |
    | Burma (Myanmar) |  Burma |
    | Bosnia-Herzegovina | Bosnia and Herzegovina |

5. Africa Continent population is replaced by the sum of `Middle East - North Africa` and `Sub-Saharan Africa`
 


