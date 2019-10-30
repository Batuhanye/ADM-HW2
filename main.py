#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 23:01:26 2019

@author: ujafarli
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Question R1
datamatches_RQ1 = pd.read_json("matches_England.json")
datalabels_RQ1 = datamatches_RQ1['label'] #this is the column for matches and scores
datalabels_RQ1 

datalabels_RQ1.isnull().sum() #we don't have any missing values which is good

a_RQ1 = []
for i in datalabels_RQ1:
    i = i.replace('-','$$$').replace(',','$$$').split('$$$')
    a_RQ1.append(i)
a_RQ1 #splitted the data from '-' and ',' and appended them into an empty list

for i in a_RQ1:
    i[0] = i[0][:-1]
    i[1] = i[1][+1:]
    i[2] = int(i[2])
    i[3] = int(i[3])
a_RQ1 #fixed the blanks on each element of the list

x_RQ1 = []
for i in a_RQ1:
    x_RQ1.append(i[0])
datamatches_RQ1['team1'] = x_RQ1
y_RQ1 = []
for i in a_RQ1:
    y_RQ1.append(i[1])
datamatches_RQ1['team2'] = y_RQ1
z_RQ1 = []
for i in a_RQ1:
    z_RQ1.append(i[2])
datamatches_RQ1['team1goal'] = z_RQ1
t_RQ1 = []
for i in a_RQ1:
    t_RQ1.append(i[3])
datamatches_RQ1['team2goal'] = t_RQ1
datamatches_RQ1.drop('label',axis=1)   #dropped the columnd and 

#finally appended the teams and scored individually to the main dataframe


weekno_RQ1 = max(datamatches_RQ1['gameweek'])
teamslist_RQ1 = list(datamatches_RQ1['team1'].unique())
scores_RQ1 = {}
for team_RQ1 in teamslist_RQ1:
    scores_RQ1[team_RQ1] = (weekno_RQ1)*[0]
    
#created empty dictionary for each team for 38 matches so that we can manipulate later
    
for week_RQ1 in range(weekno_RQ1):
    #this is a loop for manipulating every team's every element for 38 weeks
    week_data_RQ1 = datamatches_RQ1[datamatches_RQ1['gameweek'] == (week_RQ1 + 1)]
    for i in range(week_data_RQ1.shape[0]):
        s1_RQ1 = week_data_RQ1['team1goal'].to_list()
        s2_RQ1 = week_data_RQ1['team2goal'].to_list()
        t1_RQ1 = week_data_RQ1['team1'].to_list()[i]
        t2_RQ1 = week_data_RQ1['team2'].to_list()[i]
        if s1_RQ1[i] > s2_RQ1[i]:
            #if first team scored better than the second
            scores_RQ1[t1_RQ1][week_RQ1] += 3    #add three points to first
        elif s1_RQ1[i] < s2_RQ1[i]:              #if second team scored better than the first
            scores_RQ1[t2_RQ1][week_RQ1] += 3                  #add three points to second
        else:                                    #if it's a tie
            scores_RQ1[t1_RQ1][week_RQ1] += 1                  #add one point to each
            scores_RQ1[t2_RQ1][week_RQ1] += 1  
            
            
cumulative_scores_RQ1 = {}
key_RQ1 = scores_RQ1.keys()
lst_RQ1 = []
for team_RQ1 in key_RQ1:
    cumulative_scores_RQ1[team_RQ1] = np.cumsum(scores_RQ1[team_RQ1])
    #cumulative sum for each team
    
import collections

value_RQ1 = cumulative_scores_RQ1.values()
freqlist_RQ1 = []
for team_RQ1 in key_RQ1:
         temp_RQ1 = collections.Counter(cumulative_scores_RQ1[team_RQ1])
         #occurence of each point in cumulative sum
         freqlist_RQ1.append(temp_RQ1)
for i in range(len(freqlist_RQ1)):
    #printing the maximum occurence for each team's points
    print(teamslist_RQ1[i],max(freqlist_RQ1[i].values()))  
#the lowest are west bromwich albion and crystal palace
#highest ones are manchester united and manchester city(also validated from plot)


gameweeks_RQ1 = list(datamatches_RQ1['gameweek'].unique())
plt.figure(figsize=(10,10))
for team_RQ1 in cumulative_scores_RQ1:
    plt.plot(cumulative_scores_RQ1[team_RQ1],label=team_RQ1,linewidth=2)
plt.xticks(range(0,len(gameweeks_RQ1)))       #fixing x axis' ticks
plt.legend()
plt.grid()          
            
            
# Question R2
            
datamatches_RQ2 = pd.read_json("matches_England.json")
datamatches_RQ2['teamsData'][0] 
#every row contains two teams' values, we need 'side' and 'score' values from them
            
listy_RQ2 = []
for i in range (len(datamatches_RQ2['teamsData'])):
    #this loop appends the teamid,side,score,a for each team to the list 
    #where a is just for size of the list where we can manipulate later and put win/lose/draw
    for j in list(datamatches_RQ2['teamsData'][i]):
        listy_RQ2.append(j)
        listy_RQ2.append(datamatches_RQ2['teamsData'][i][j]['side'])
        listy_RQ2.append(datamatches_RQ2['teamsData'][i][j]['score'])
        listy_RQ2.append('a')
        

listy_RQ2 = np.array(listy_RQ2)
#turning the list into array
listy_RQ2 = listy_RQ2.reshape((len(datamatches_RQ2['teamsData']),8))
#8 because 4 for each team:teamid,side,score,result
print(listy_RQ2[0])


for i in range(len(datamatches_RQ2['teamsData'])):
    #this is for changing a's into win/lose or draw according to scores
    if listy_RQ2[i][2] > listy_RQ2[i][6]:
        listy_RQ2[i][3] = 'win' 
        listy_RQ2[i][7] = 'lose'
    if listy_RQ2[i][2] < listy_RQ2[i][6]:
        listy_RQ2[i][3] = 'lose'
        listy_RQ2[i][7] = 'win'
    elif listy_RQ2[i][2] == listy_RQ2[i][6]:
        listy_RQ2[i][3] = 'draw' 
        listy_RQ2[i][7] = 'draw'
        

listy_RQ2=pd.DataFrame(listy_RQ2)                      #converting the list into data frame
listy_RQ2.columns=['ID_1','Pos_1','Score_1','Result_1',
              'ID_2','Pos_2','Score_2','Result_2']     #naming the columns to work easier
print(listy_RQ2)         

#I picked first 5 teams '1646','1628','1609','1651','1644'
#each team could be either on ID_1 or ID_2 so for each case I created two series and excluded the matches between all teams
df1_RQ2 = listy_RQ2[(listy_RQ2['ID_1']=='1646') & ( listy_RQ2['ID_2']!='1628') & (listy_RQ2['ID_2']!='1609') & (listy_RQ2['ID_2']!='1651') & (listy_RQ2['ID_2']!='1644')]
df1_RQ2 = df1_RQ2.groupby(['Pos_1','Result_1']).count().ID_1
df2_RQ2 = listy_RQ2[(listy_RQ2['ID_2']=='1646') & ( listy_RQ2['ID_1']!='1628') & (listy_RQ2['ID_1']!='1609') & (listy_RQ2['ID_1']!='1651') & (listy_RQ2['ID_1']!='1644')]
df2_RQ2 = df2_RQ2.groupby(['Pos_2','Result_2']).count().ID_2
Ctable1_RQ2 = df1_RQ2.append(df2_RQ2)#appended them
Ctable1_RQ2 = Ctable1_RQ2.sum(level=[0,1])#summed them on two levels which are position(home,away) and result(win,draw,lose)
#and summed the results in each case
df1_RQ2 = listy_RQ2[(listy_RQ2['ID_1']=='1628') & ( listy_RQ2['ID_2']!='1646') & (listy_RQ2['ID_2']!='1609') & (listy_RQ2['ID_2']!='1651') & (listy_RQ2['ID_2']!='1644')]
df1_RQ2 = df1_RQ2.groupby(['Pos_1','Result_1']).count().ID_1
df2_RQ2 = listy_RQ2[(listy_RQ2['ID_2']=='1628') & ( listy_RQ2['ID_1']!='1646') & (listy_RQ2['ID_1']!='1609') & (listy_RQ2['ID_1']!='1651') & (listy_RQ2['ID_1']!='1644')]
df2_RQ2 = df2_RQ2.groupby(['Pos_2','Result_2']).count().ID_2
Ctable2_RQ2 = df1_RQ2.append(df2_RQ2)
Ctable2_RQ2 = Ctable2_RQ2.sum(level=[0,1])
df1_RQ2 = listy_RQ2[(listy_RQ2['ID_1']=='1609') & ( listy_RQ2['ID_2']!='1646') & (listy_RQ2['ID_2']!='1628') & (listy_RQ2['ID_2']!='1651') & (listy_RQ2['ID_2']!='1644')]
df1_RQ2 = df1_RQ2.groupby(['Pos_1','Result_1']).count().ID_1
df2_RQ2 = listy_RQ2[(listy_RQ2['ID_2']=='1609') & ( listy_RQ2['ID_1']!='1646') & (listy_RQ2['ID_1']!='1628') & (listy_RQ2['ID_1']!='1651') & (listy_RQ2['ID_1']!='1644')]
df2_RQ2 = df2_RQ2.groupby(['Pos_2','Result_2']).count().ID_2
Ctable3_RQ2 = df1_RQ2.append(df2_RQ2)
Ctable3_RQ2 = Ctable3_RQ2.sum(level=[0,1])
df1_RQ2 = listy_RQ2[(listy_RQ2['ID_1']=='1651') & ( listy_RQ2['ID_2']!='1646') & (listy_RQ2['ID_2']!='1628') & (listy_RQ2['ID_2']!='1609') & (listy_RQ2['ID_2']!='1644')]
df1_RQ2 = df1_RQ2.groupby(['Pos_1','Result_1']).count().ID_1
df2_RQ2 = listy_RQ2[(listy_RQ2['ID_2']=='1651') & ( listy_RQ2['ID_1']!='1646') & (listy_RQ2['ID_1']!='1628') & (listy_RQ2['ID_1']!='1609') & (listy_RQ2['ID_1']!='1644')]
df2_RQ2 = df2_RQ2.groupby(['Pos_2','Result_2']).count().ID_2
Ctable4_RQ2 = df1_RQ2.append(df2_RQ2)
Ctable4_RQ2 = Ctable4_RQ2.sum(level=[0,1])
df1_RQ2 = listy_RQ2[(listy_RQ2['ID_1']=='1644') & ( listy_RQ2['ID_2']!='1646') & (listy_RQ2['ID_2']!='1628') & (listy_RQ2['ID_2']!='1609') & (listy_RQ2['ID_2']!='1651')]
df1_RQ2 = df1_RQ2.groupby(['Pos_1','Result_1']).count().ID_1
df2_RQ2 = listy_RQ2[(listy_RQ2['ID_2']=='1644') & ( listy_RQ2['ID_1']!='1646') & (listy_RQ2['ID_1']!='1628') & (listy_RQ2['ID_1']!='1609') & (listy_RQ2['ID_1']!='1651')]
df2_RQ2 = df2_RQ2.groupby(['Pos_2','Result_2']).count().ID_2
Ctable5_RQ2 = df1_RQ2.append(df2_RQ2)
Ctable5_RQ2 = Ctable5_RQ2.sum(level=[0,1])
Ctableall_RQ2 = Ctable1_RQ2.append([Ctable2_RQ2,Ctable3_RQ2,Ctable4_RQ2,Ctable5_RQ2])#after getting results for each team, appended them and
Ctableall_RQ2 = Ctableall_RQ2.sum(level=[0,1])#summed them on two levels which are position(home,away) and result(win,draw,lose)


np1_RQ2 = np.array(Ctableall_RQ2[0:3])
np2_RQ2 = np.array(Ctableall_RQ2[3:6])
final_table_RQ2 = np.array([np1_RQ2,np2_RQ2])
from scipy import stats
#we have null hypothesis as:playing at home or away does not affect the outcome of the match, and h1 as they affect the outcome
chi2_stat, p_val, dof, ex = stats.chi2_contingency(final_table_RQ2)
print("Chi2 Stat")
print(chi2_stat)
print("\n")
print("Degrees of Freedom")
print(dof)
print("\n")
print("P-Value")
print(p_val)
print("\n")
            
            
# Question R3
#coaches data base
coaches_RQ3 = pd.read_json("coaches.json")
teams_RQ3 = pd.read_json("teams.json")
coaches_RQ3.head()
coaches_RQ3 = pd.DataFrame(coaches_RQ3)
coaches_RQ3.head(10)

#dataframe of area inside coaches
birtharea_RQ3 = list(coaches_RQ3['birthArea'])
birtharea_RQ3 = pd.DataFrame(birtharea_RQ3)
birtharea_RQ3.head()

#dataframe of area inside teams
teamsarea_RQ3 = list(teams_RQ3['area'])
teamsarea_RQ3 = pd.DataFrame(teamsarea_RQ3)
teamsarea_RQ3.head()

#teams database
teams_RQ3 = pd.DataFrame(teams_RQ3)
teams_RQ3.head(20)
club_RQ3 = teams_RQ3.rename(columns={"name": "club"})
club_RQ3 = club_RQ3.join(teamsarea_RQ3)
clubdf_RQ3 = pd.DataFrame(club_RQ3, columns=['wyId','officialName','club','name'])
clubdf_RQ3.head(10)



#coaches and team join by wyId and current teams id
merge_RQ3 = pd.merge(teams_RQ3, coaches_RQ3 , left_on='wyId', right_on='currentTeamId',how='inner')
merge_RQ3 = pd.DataFrame(merge_RQ3, columns=['wyId_x', 'officialName','wyId_y','shortName','birthDate'])
merge_RQ3.head(10)


#Take only data about premier league
england_RQ3 = pd.merge_RQ3(merge_RQ3, clubdf_RQ3, on='officialName')
england_RQ3 = pd.DataFrame(england_RQ3, columns=['wyId', 'officialName', 'name','wyId_y','shortName','birthDate'])
england_RQ3 = england_RQ3.rename(columns={"wyId": "IdClub", 'wyId_y': 'IdCoaches', 'name':'areaTeam'})
england_RQ3 = england_RQ3.loc[england_RQ3['areaTeam'] == 'England']

england_RQ3  #=england.drop(0, axis=0)

#calculate age of each coaches
from datetime import date

a_RQ3 = list(england_RQ3['birthDate'].str.split('-'))

def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) <  (birthDate.month, birthDate.day)) 
  
    return age 
age = []  
for i in range(len(a_RQ3)):
    age.append(calculateAge(date(int(a_RQ3[i][0]), int(a_RQ3[i][1]), int(a_RQ3[i][2]) )))
age = pd.DataFrame(age)

#Distribution of  the ages of all coaches in Premier League

plt.plot(england_RQ3['officialName'], age[0])
plt.grid()
plt.ylabel("age of coaches")
plt.xlabel("team")

plt.xticks(rotation='vertical')
plt.show()

#10 teams with the youngest coaches.
engSort=england_RQ3.sort_values(by=['birthDate'], ascending=False).head(10)


ageSort=age.sort_values(by=[0]).head(10)

#10 teams with the youngest coaches
plt.bar(engSort['officialName'],ageSort[0])
plt.ylabel("age of coaches")
plt.xlabel("team")

plt.xticks(rotation='vertical')

plt.show()

# Question R4
# Read json files
players_RQ4 = pd.read_json('players.json')
events_RQ4 = pd.read_json('events_England.json')
teams_RQ4 = pd.read_json('teams.json')

players_RQ4 = players_RQ4.rename(columns = {'wyId':'playerId', 'currentTeamId':'teamId'})

# New table about Players
df1_RQ4 = players_RQ4[['firstName', 'lastName', 'height', 'playerId', 'teamId']]
df2_RQ4 = events_RQ4[['playerId', 'teamId', 'tags', 'eventName', 'subEventName']]


# Take only England
area_RQ4 = list(teams_RQ4['area'])
area_RQ4 = pd.DataFrame(area_RQ4)
area_RQ4.head()
teams_RQ4 = teams_RQ4.rename(columns = {'name':'team_name', 'wyId':'teamId'})
area_RQ4 = area_RQ4[['name']]
teams_RQ4 = teams_RQ4[['team_name','teamId']]
area_RQ4 =  area_RQ4.join(teams_RQ4)
# England wyId is ?
area_RQ4 = area_RQ4[area_RQ4.name == 'England']
# Take only with England ID
x1_RQ4 = pd.merge(area_RQ4, df2_RQ4 , on = 'teamId',how='inner')
merge_RQ4 = pd.merge(df1_RQ4, x1_RQ4 , on = 'playerId',how='inner')   #attempted
accurate_RQ4 = merge_RQ4[merge_RQ4["tags"].str[-1].str["id"]==1801]   #accurate


#only unique players in all players
# take id of all kind of players
all_players_RQ4 = merge_RQ4[['playerId']]
all_players_RQ4 = all_players_RQ4.drop_duplicates(subset='playerId', keep="first")
all_players_RQ4.sort_values(by=['playerId'], inplace=True)
# find how much per player 
df_all_RQ4 = merge_RQ4.groupby(['playerId'])['playerId'].size()
df_all_RQ4 = df_all_RQ4.rename(columns = {'playerId':'countAll'})

# take id of all accurate players
accurate_players_RQ4 = accurate_RQ4[['playerId']]
accurate_players_RQ4 = accurate_players_RQ4.drop_duplicates(subset='playerId', keep="first")
accurate_players_RQ4.sort_values(by=['playerId'], inplace=True)
# find how much accurate pass per player
df_accurate_RQ4 = accurate_RQ4.groupby(['playerId'])['playerId'].size()

final_data_RQ4 = pd.concat([df_accurate_RQ4, df_all_RQ4], axis=1)


# Question 5
# Read json files
players_RQ5 = pd.read_json('players.json')
events_RQ5 = pd.read_json('events_England.json')
teams_RQ5 = pd.read_json('teams.json')

players_RQ5 = players_RQ5.rename(columns = {'wyId':'playerId', 'currentTeamId':'teamId'})

# New table about Players
df1_RQ5 = players_RQ5[['firstName', 'lastName', 'height', 'playerId', 'teamId']]
df2_RQ5 = events_RQ5[['playerId', 'teamId', 'tags', 'eventName', 'subEventName']]


# Take only England
area_RQ5 = list(teams_RQ5['area'])
area_RQ5 = pd.DataFrame(area_RQ5)
area_RQ5.head()
teams_RQ5 = teams_RQ5.rename(columns = {'name':'team_name', 'wyId':'teamId'})
area_RQ5 = area_RQ5[['name']]
teams_RQ5 = teams_RQ5[['team_name','teamId']]
area_RQ5 =  area_RQ5.join(teams_RQ5)
# England wyId is ?
area_RQ5 = area_RQ5[area_RQ5.name == 'England']

x1_RQ5 = pd.merge(area_RQ5, df2_RQ5 , on = 'teamId',how='inner')
merge_RQ5 = pd.merge(df1_RQ5, x1_RQ5 , on = 'playerId',how='inner')



# Calculate ratio

unique_Players_RQ5 = merge_RQ5[['firstName', 'lastName', 'playerId', 'height', 'name']]
unique_Players_RQ5 = unique_Players_RQ5.drop_duplicates()
# Calculate ratio
unique_Players_RQ5['count_accurate'] = [0 for i in range(len(unique_Players_RQ5))]
unique_Players_RQ5['count_not_accurate'] = [0 for i in range(len(unique_Players_RQ5))]

count_accurate_RQ5 = 0
count_not_accurate_RQ5 = 0

# Question R6

# Core Question 1 
matches_England_CQ1 = pd.read_json("matches_England.json")
matches_England_CQ1 = pd.DataFrame(matches_England_CQ1)
#, columns=['wyId','firstName','lastName','role'])
matches_England_CQ1.head()

events_England_CQ1 = pd.read_json("events_England.json")
events_England_CQ1 = pd.DataFrame(events_England_CQ1)


england_CQ1 = pd.merge(events_England_CQ1, matches_England_CQ1, left_on='matchId', right_on='nameClub')
england_CQ1 = pd.DataFrame(england_CQ1, columns=['eventId','eventName','eventSec','matchPeriod','subEventName','subEventId','label','teamsData','tags','nameClub'])

en_CQ1 = england_CQ1[england_CQ1['tags'].str[0].str['id']==101]
shotEn_CQ1 = en_CQ1[en_CQ1['eventName']=='Shot']
saveAttEn_CQ1 = en_CQ1[en_CQ1['eventName']=='Save attempt']

penalty_CQ1 = en_CQ1[en_CQ1['subEventName']=='Penalty']


f=(shotEn_CQ1, penalty_CQ1)
shotEngland_CQ1 = pd.concat(f)
shotEngland_CQ1 = shotEngland_CQ1.sort_values(by=['nameClub'])

print(saveAttEn_CQ1)

frames_CQ1 = (saveAttEn_CQ1, shotEngland_CQ1)
goalEn_CQ1 = pd.concat(frames_CQ1)

goalEn_CQ1 = goalEn_CQ1.sort_values(by=['nameClub'])

goalEn_CQ1.head()

#second to min
goalEn_CQ1['eventSec'].update(goalEn_CQ1['eventSec']/60)

fristTime_CQ1 = goalEn_CQ1[goalEn_CQ1['matchPeriod']=='1H']
secondTime_CQ1 = goalEn_CQ1[goalEn_CQ1['matchPeriod']=='2H']

range1=len(fristTime_CQ1[fristTime_CQ1['eventSec'].between(0, 9, inclusive=False)])
range2=len(fristTime_CQ1[fristTime_CQ1['eventSec'].between(9, 18, inclusive=False)])
range3=len(fristTime_CQ1[fristTime_CQ1['eventSec'].between(18, 27, inclusive=False)])
range4=len(fristTime_CQ1[fristTime_CQ1['eventSec'].between(27, 36, inclusive=False)])
range5=len(fristTime_CQ1[fristTime_CQ1['eventSec'].between(36, 45, inclusive=False)])
range6=len(fristTime_CQ1[fristTime_CQ1['eventSec']>45])

range7=len(secondTime_CQ1[secondTime_CQ1['eventSec'].between(0, 9, inclusive=False)])
range8=len(secondTime_CQ1[secondTime_CQ1['eventSec'].between(9, 18, inclusive=False)])
range9=len(secondTime_CQ1[secondTime_CQ1['eventSec'].between(18, 27, inclusive=False)])
range10=len(secondTime_CQ1[secondTime_CQ1['eventSec'].between(27, 36, inclusive=False)])
range11=len(secondTime_CQ1[secondTime_CQ1['eventSec'].between(36, 45, inclusive=False)])
range12=len(secondTime_CQ1[secondTime_CQ1['eventSec']>45])

slot_CQ1 = {'timeSlot':[('0-9'),('9-18'),('18-27'),('27-36'),('36-45'), '45+',('45-54'),('54-63'),('63-72'),('72-81'),('81-90'),'90+'], 
          'goal':[range1,range2,range3,range4,range5,range6,range7,range8,range9,range10,range11,range12]}

slotDf = pd.DataFrame(slot_CQ1)


plt.bar(slotDf['timeSlot'],slotDf['goal'],color=('red','purple','orange','green','yellow','cyan','lightgreen','pink','silver','lime','maroon','gold'))
plt.xticks(rotation=45)
plt.ylabel("Goal")
plt.xlabel("Time slot")

plt.show()


# Core Question 2 
#Part 1
import seaborn as sns
import matplotlib.patches as mpatches
# Read json files
players_CQ2_P1 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/players.json')
events_CQ2_P1 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/events_Spain.json')
teams_CQ2_P1 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/teams.json')
matches_CQ2_P1 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/matches_Spain.json')

# Rename columns for merging
players_CQ2_P1 = players_CQ2_P1.rename(columns = {'wyId':'playerId', 'currentTeamId':'teamId'})
matches_CQ2_P1 = matches_CQ2_P1.rename(columns = {'wyId':'matchId'})
teams_CQ2_P1 = teams_CQ2_P1.rename(columns = {'wyId':'teamId'})

# Merge DataFrames
May_CQ2_P1 = matches_CQ2_P1[matches_CQ2_P1['dateutc'].str.contains('2018-05-06')]
May_Matches_CQ2_P1 = pd.merge(events_CQ2_P1, May_CQ2_P1 , on = 'matchId',how='inner')
May_Matches_CQ2_P1 = pd.merge(May_Matches_CQ2_P1, players_CQ2_P1 , on = 'playerId',how='inner')
May_Matches_CQ2_P1 = May_Matches_CQ2_P1[['firstName','lastName','eventName', 'positions', 'subEventName', 'tags']]

# Only Lionel Messi and Cristiano Ronaldo
Ronaldo = May_Matches_CQ2_P1[May_Matches_CQ2_P1['firstName'].str.contains('Cristiano Ronaldo')]
Messi = May_Matches_CQ2_P1[May_Matches_CQ2_P1['lastName'].str.contains('Messi')]

Ronaldo['eventName'].unique()#checking which events ronaldo has

Messi['eventName'].unique()#checking which events messi has         
            
 #deleting other rows except pass,duel,shot,freekick
delete_balls_CQ2_P1 = Ronaldo[Ronaldo['eventName']=='Others on the ball'].index
delete_offsides_CQ2_P1 = Ronaldo[Ronaldo['eventName']=='Offside'].index
Ronaldo = Ronaldo.drop(delete_balls_CQ2_P1)
Ronaldo = Ronaldo.drop(delete_offsides_CQ2_P1)
#creating a temporary list to extrach the positions of Ronaldo
listy_CQ2_P1 = []
for key, value in Ronaldo['positions'].iteritems():
    temp_CQ2_P1 = [key,value[0]['y'],value[0]['x'],value[1]['y'],value[1]['x']]
    listy_CQ2_P1.append(temp_CQ2_P1)
#and appending them 1 by 1 to new columns
a_CQ2_P1 = []
for i in listy_CQ2_P1:
    a_CQ2_P1.append(i[1])
b_CQ2_P1 = []
for i in listy_CQ2_P1:
    b_CQ2_P1.append(i[2])
c_CQ2_P1 = []
for i in listy_CQ2_P1:
    c_CQ2_P1.append(i[3])
d_CQ2_P1 = []
for i in listy_CQ2_P1:
    d_CQ2_P1.append(i[4])
Ronaldo['yfirst'] = a_CQ2_P1
Ronaldo['xfirst'] = b_CQ2_P1
Ronaldo['ysecond'] = c_CQ2_P1
Ronaldo['xsecond'] = d_CQ2_P1

#same for Messi
delete_balls_CQ2_P1 = Messi[Messi['eventName']=='Others on the ball'].index
delete_offsides_CQ2_P1 = Messi[Messi['eventName']=='Offside'].index
delete_fouls_CQ2_P1 = Messi[Messi['eventName']=='Foul'].index
Messi = Messi.drop(delete_balls_CQ2_P1)
Messi = Messi.drop(delete_offsides_CQ2_P1)
Messi = Messi.drop(delete_fouls_CQ2_P1)
listyx_CQ2_P1 = []
for key, value in Messi['positions'].iteritems():
    temp_CQ2_P1 = [key,value[0]['y'],value[0]['x'],value[1]['y'],value[1]['x']]
    listyx_CQ2_P1.append(temp_CQ2_P1)
a_CQ2_P1 = []
for i in listyx_CQ2_P1:
    a_CQ2_P1.append(i[1])
b_CQ2_P1 = []
for i in listyx_CQ2_P1:
    b_CQ2_P1.append(i[2])
c_CQ2_P1 = []
for i in listyx_CQ2_P1:
    c_CQ2_P1.append(i[3])
d_CQ2_P1 = []
for i in listyx_CQ2_P1:
    d_CQ2_P1.append(i[4])
Messi['yfirst'] = a_CQ2_P1
Messi['xfirst'] = b_CQ2_P1
Messi['ysecond'] = c_CQ2_P1
Messi['xsecond'] = d_CQ2_P1           
     
#a function for fuutball pitch
def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = mpatches.Rectangle([0,0], width = 120, height = 80, fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = mpatches.Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = mpatches.Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    midline = mpatches.ConnectionPatch([60,0], [60,80], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = mpatches.Rectangle([0,32], width = 4.9, height = 16, fill = False)
    RightSixYard = mpatches.Rectangle([115.1,32], width = 4.9, height = 16, fill = False)


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = mpatches.Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = mpatches.Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)
fig=plt.figure() #set up the figures
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax) #overlay our different objects on the pitch
plt.ylim(-2, 90)
plt.xlim(-2, 130)
plt.axis('off')

sns.kdeplot(Ronaldo['xfirst'],Ronaldo["yfirst"], shade=True,n_levels=50) #highlighting the plot with Ronaldo's movements
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.show()


fig=plt.figure() #set up the figures
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax) #overlay our different objects on the pitch
plt.ylim(-2, 90)
plt.xlim(-2, 130)
plt.axis('off')

sns.kdeplot(Messi['xfirst'],Messi["yfirst"], shade=True,n_levels=50)#highlighting the plot with Messi's movements
plt.ylim(-2, 82)
plt.xlim(-2, 122)

plt.show()
#Messi played close to the center circle while Ronaldo played right side of the field. Ronaldo played in more expansely while Messi was more stationary.       
# Core Question 2 
#Part 2       

#Reading the files for Italy's matches
events_CQ2_P2 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/events_Italy.json')
matches_CQ2_P2 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/matches_Italy.json')
players_CQ2_P2 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/players.json')
teams_CQ2_P2 = pd.read_json('C:/Users/User/Desktop/ADM/HW2/Files/teams.json')


# Rename columns for merging
players_CQ2_P2 = players_CQ2_P2.rename(columns = {'wyId':'playerId', 'currentTeamId':'teamId'})
matches_CQ2_P2 = matches_CQ2_P2.rename(columns = {'wyId':'matchId'})
teams_CQ2_P2 = teams_CQ2_P2.rename(columns = {'wyId':'teamId'})

# Merge DataFrames
Apr_CQ2_P2 = matches_CQ2_P2[matches_CQ2_P2['dateutc'].str.contains('2018-04-22')]
Apr_Matches_CQ2_P2 = pd.merge(events_CQ2_P2, Apr_CQ2_P2 , on = 'matchId',how='inner')
Apr_Matches_CQ2_P2 = pd.merge(Apr_Matches_CQ2_P2, players_CQ2_P2 , on = 'playerId',how='inner')
Apr_Matches_CQ2_P2 = Apr_Matches_CQ2_P2[['firstName','lastName','eventName', 'positions', 'subEventName', 'tags']]

# Only Jorginho and Miralem Pjanic
Jorginho = Apr_Matches_CQ2_P2[Apr_Matches_CQ2_P2['firstName'].str.contains('Jorge Luiz')]
Miralem = Apr_Matches_CQ2_P2[Apr_Matches_CQ2_P2['firstName'].str.contains('Miralem')]

#getting only passes for each player
Jorginho = Jorginho[Jorginho['eventName']=='Pass']
Miralem = Miralem[Miralem['eventName']=='Pass']
#creating a temporary list to extrach the positions of Jorginho
listy_CQ2_P2 = []
for key, value in Jorginho['positions'].iteritems():
    temp_CQ2_P2 = [key,value[0]['y'],value[0]['x'],value[1]['y'],value[1]['x']]
    listy_CQ2_P2.append(temp_CQ2_P2)
#and appending them 1 by 1 to new columns
a_CQ2_P2 = []
for i in listy_CQ2_P2:
    a_CQ2_P2.append(i[1])
b_CQ2_P2 = []
for i in listy_CQ2_P2:
    b_CQ2_P2.append(i[2])
c_CQ2_P2 = []
for i in listy_CQ2_P2:
    c_CQ2_P2.append(i[3])
d_CQ2_P2 = []
for i in listy_CQ2_P2:
    d_CQ2_P2.append(i[4])
Jorginho['yfirst'] = a_CQ2_P2
Jorginho['xfirst'] = b_CQ2_P2
Jorginho['ysecond'] = c_CQ2_P2
Jorginho['xsecond'] = d_CQ2_P2
#same for Miralem
listyx_CQ2_P2 = []
for key, value in Miralem['positions'].iteritems():
    temp_CQ2_P2 = [key,value[0]['y'],value[0]['x'],value[1]['y'],value[1]['x']]
    listyx_CQ2_P2.append(temp_CQ2_P2)
a_CQ2_P2 = []
for i in listyx_CQ2_P2:
    a_CQ2_P2.append(i[1])
b_CQ2_P2 = []
for i in listyx_CQ2_P2:
    b_CQ2_P2.append(i[2])
c_CQ2_P2 = []
for i in listyx_CQ2_P2:
    c_CQ2_P2.append(i[3])
d_CQ2_P2 = []
for i in listyx_CQ2_P2:
    d_CQ2_P2.append(i[4])
Miralem['yfirst'] = a_CQ2_P2
Miralem['xfirst'] = b_CQ2_P2
Miralem['ysecond'] = c_CQ2_P2
Miralem['xsecond'] = d_CQ2_P2
#These are only accurate passes
Jorginho_Accurate = Jorginho[Jorginho["tags"].str[-1].str["id"]==1801]
Miralem_Accurate = Miralem[Miralem["tags"].str[-1].str["id"]==1801]

  

fig=plt.figure() #set up the figures
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax) #overlay our different objects on the pitch
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
for i in range(len(Jorginho)):
    # annotate draw an arrow from a first position to second position
    ax.annotate("", xy = (Jorginho['ysecond'].values[i], Jorginho['xsecond'].values[i]), xycoords = 'data',
               xytext = (Jorginho['yfirst'].values[i], Jorginho['xfirst'].values[i]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"),)
for i in range(len(Miralem)):
    ax.annotate("", xy = (Miralem['ysecond'].values[i], Miralem['xsecond'].values[i]), xycoords = 'data',
               xytext = (Miralem['yfirst'].values[i], Miralem['xfirst'].values[i]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"),)
plt.show()
#red lines are for Miralem while blue lines are for Jorginho
fig=plt.figure() #set up the figures
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax) #overlay our different objects on the pitch
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
for i in range(len(Jorginho)):
    # annotate draw an arrow from a first position to second position
    ax.annotate("", xy = (Jorginho['ysecond'].values[i], Jorginho['xsecond'].values[i]), xycoords = 'data',
               xytext = (Jorginho['yfirst'].values[i], Jorginho['xfirst'].values[i]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"),)
for i in range(len(Jorginho_Accurate)):
    ax.annotate("", xy = (Jorginho_Accurate['ysecond'].values[i], Jorginho_Accurate['xsecond'].values[i]), xycoords = 'data',
               xytext = (Jorginho_Accurate['yfirst'].values[i], Jorginho_Accurate['xfirst'].values[i]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"),)

sns.kdeplot(Jorginho['yfirst'],Jorginho["xfirst"], shade=True,n_levels=50)#coordinates of x and y's are switched so I reversed them

plt.show()
#the above plot is just for Jorginho
#red lines are accurate passes while blue ones are inaccurate, there is a huge difference between them

fig=plt.figure() #set up the figures
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax) #overlay our different objects on the pitch
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
for i in range(len(Miralem)):
    # annotate draw an arrow from a first position to second position
    ax.annotate("", xy = (Miralem['ysecond'].values[i], Miralem['xsecond'].values[i]), xycoords = 'data',
               xytext = (Miralem['yfirst'].values[i], Miralem['xfirst'].values[i]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "blue"),)
for i in range(len(Miralem_Accurate)):
    ax.annotate("", xy = (Miralem_Accurate['ysecond'].values[i], Miralem_Accurate['xsecond'].values[i]), xycoords = 'data',
               xytext = (Miralem_Accurate['yfirst'].values[i], Miralem_Accurate['xfirst'].values[i]), textcoords = 'data',
               arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = "red"),)
sns.kdeplot(Miralem['xfirst'],Miralem["yfirst"], shade=True,n_levels=50)
plt.show()

# the above plot is just for Miralem
#red lines are accurate passes while blue ones are inaccurate, it seems there's only one visible inaccurate pass




