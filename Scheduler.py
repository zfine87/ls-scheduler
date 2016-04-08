import csv, time, datetime

#Class for HLTV player
class Shift:

  #Constructor
  def __init__(self, name, start, end, day, rank):
    self.name = name
    self.start = start
    self.end = end
    self.day = day
    self.rank = rank

class Intern:

  def __init__(self, name, rank):
    self.name = name
    self.rank = rank

def getRankings():
  rankList = []

  with open('rankings.csv', newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)
    for each in spamreader:
      rankList.append(Intern(each[0], each[1]))

  return rankList

def getSchedule(rankList):
  shiftList = []

  with open('schedules.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader, None)
    for each in spamreader:
      shiftList.append(Shift(each[1], datetime.datetime.strptime(str(each[0]) + " " +str(each[2]), "%m/%d/%Y %I:%M %p" ), datetime.datetime.strptime(str(each[0]) + " " +str(each[3]), "%m/%d/%Y %I:%M %p" ), datetime.datetime.strptime(each[0], "%m/%d/%Y"), next((x.rank for x in rankList if x.name == each[1]), None) ) )

  return shiftList



def createSchedule(scheduleList):

  dayList = sorted(list(set([each.day for each in scheduleList])))

  for day in dayList:
    workList = []
    change = False

    newScheduleList = [shift for shift in scheduleList if shift.day == day]

    newScheduleList.sort(key=lambda x: x.start, reverse=False)
    time = day
    while(time < day + datetime.timedelta(days=1)):
      #Check for and remove ending shifts
      newWorkList = [shift for shift in workList if shift.end != time]
      if(len(newWorkList) != len(workList)):
        change = True

      workList = newWorkList

      #Check for and add new shifts
      for shift in newScheduleList:
        if shift.start == time:
          addShift(workList, shift)
          change = True
          
      if(change):
        printWorkList(workList, time)

      change = 0
      time += datetime.timedelta(minutes=15)

    print(str(day))
    input()

#Add new shift into list, then reorder based on ranking
def addShift(workList, shift):
  workList.append(shift)
  workList.sort(key=lambda x: x.rank, reverse=False)  
  

def printWorkList(workList, time):
  print()
  print(time.strftime("At %I:%M %p"))
  size = len(workList)
  for i in range(0, int(size/3)):
    print(workList[i].name + " in Group 3")
  for i in range(int(size/3), int((size/3) * 2)):
    print(workList[i].name + " in Group 2")
  for i in range(int((size/3)*2), int((size/3) * 3)):
    print(workList[i].name + " in Group 1")


# getSchedule()
createSchedule(getSchedule(getRankings()))