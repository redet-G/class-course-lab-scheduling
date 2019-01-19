# represent courses
class course():
	MAX_LAB_HOURS =  4
	def __init__(self, name, creditHoure, labCredit = 0):
		self.name = name
		self.creditHoure = creditHoure
		self.labCredit = labCredit
		self.teacher = []
		self.numberOfSections = 0
	def add(self,teacher):
		self.teacher.append(teacher)
	def getPeriods(self):
		periods = []
		for t in self.teacher:
			periods.extend(t.getPeriods(self))
		return periods
	def hasLab(self):
		return self.labCredit!=0
	# return lab periods 
	def getLabPeriod(self):
		periods = []
		if self.hasLab():
			numberOfPeriods = int(self.labCredit/course.MAX_LAB_HOURS)
			for i in range(numberOfPeriods):
				periods.append(Period(self.teacher[0],self,course.MAX_LAB_HOURS,True))
			leftoverLabSession = self.labCredit%course.MAX_LAB_HOURS
			if leftoverLabSession!=0:
				periods.append(Period(self.teacher[0],self,leftoverLabSession,True))
		return periods
	def __eq__(self,other):
		if other == None:
			return False
		return self.name == other.name and self.creditHoure == other.creditHoure and self.labCredit and other.teacher
	def __str__(self):
		return self.name
class section():
	def __init__(self,name,semester,year,courses):
		self.name = name 
		self.year = year
		self.semester = semester
		self.courses = courses
		self.busyMatrix = [
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False]
			]
		for course in courses:
			course.numberOfSections += 1
	def __eq__(self, other):
		return self.name == other.name and self.year == other.year and self.semester == other.semester
	def __str__(self):
		return self.name
	def isFreeAt(self,day,time,n):
		try:
			logic = True
			for i in range(0,n,1):
				logic = ( not self.busyMatrix[day][time+i] )and logic
			return logic
		except:
			return False
	def setBusy(self,day,time,n):
		for i in range(0,n,1):
			self.busyMatrix[day][time+i]=True
# represents the class bing thought at a specific class with a specific teacher 
class Period():
	def __init__(self, teacher, course, length,isLab = False):
		self.teacher = teacher
		self.course = course
		self.length = length
		self.section = None
		self.isLab = isLab
	def __eq__(self, other):
		if other == None:
			return False
		return self.teacher == other.teacher and self.course == other.course
	def __str__(self):
		if self.isLab:
			return "lab"+str(self.course.name)+str(self.section)
		else:
			return str(self.course.name)+str(self.section)
class Room():
	def __init__(self,name, isLab=False):
		self.name = name
		self.isLab = isLab
		self.section = []
		
		self.timeSlot = [
			[None,None,None,None,None,None,None,None],
			[None,None,None,None,None,None,None,None],
			[None,None,None,None,None,None,None,None],
			[None,None,None,None,None,None,None,None],
			[None,None,None,None,None,None,None,None],
			[None,None,None,None,None,None,None,None],
			[None,None,None,None,None,None,None,None]
		] # represents a time slot according to the index
		# index 0 indicates the first hour from 2:00 to 3:00
	def isFreeAt(self, day, time, n=1):
		try:
			logic = True
			# don't split period between lunch time
			if time < 4 and ((time + n )> 4):
				return False 
			
			if time + n > 8:
				return False
			for i in range(0, n, 1):
				logic = logic and self.timeSlot[day][time+i] == None
			return logic
		except:
			return False
	# assign a teacher to a classroom at time slot.
	# if slot is not given it will search for a free slot and place it
	def assign(self, period, day, time):
		if(self.isFreeAt(day,time,period.length)):
			if(not period.teacher.isFree(day,time,period.length)):
					return False
			for i in range(0,period.length,1):
				self.timeSlot[day][time+i] = period
				period.section.setBusy(day,time,period.length)
				period.teacher.setBusy(day,time,period.length)
			return True
		return False
	def isTeacherFree(self,teacher,day,time):
		return not self.timeSlot[day][time] in teacher.getPeriods()
	
	def number_of_available_slot(self,allowedTimeOfTheDay=[0,1,2,3,4,5,6,7],allowedDayOfTheWeek=[0,1,2,3,4]):
		freeSlots = 0
		for day in allowedDayOfTheWeek:
			for time in allowedTimeOfTheDay:
				if self.timeSlot[day][time] == None:
					freeSlots+=1
		return freeSlots
	
	def __str__(self):
		text = " room: "+self.name+"\n "
		for i in range(0,len(self.timeSlot[0]),1):
			for j in range(0,len(self.timeSlot),1):
				text += str(self.timeSlot[j][i]) + "   "
			text+=" \n "
		return text
	def __cmp__(self,other):
		return self.number_of_available_slot() - other.number_of_available_slot()
	def __lt__(self, other):
		return self.number_of_available_slot() - other.number_of_available_slot() < 0
	def __gt__(self, other):
		return self.number_of_available_slot() - other.number_of_available_slot() > 0
	def __eq__(self, other):
		return self.number_of_available_slot() - other.number_of_available_slot() == 0
	def __le__(self, other):
		return self.number_of_available_slot() - other.number_of_available_slot() <= 0
	def __ge__(self, other):
		return self.number_of_available_slot() - other.number_of_available_slot() >= 0
	def __ne__(self, other):
		return self.number_of_available_slot() - other.number_of_available_slot() != 0
		
# ranks the courses according to the teachers preference 
class coursePreference():
	def __init__(self, pref):
		self.rank = pref
	#append a new course 
	def add(self, course):
		self.rank.append(course)
		
		
# represent a teacher
class Teacher(): 
	MAX_NUMBER_OF_HOURS = 2
	def __init__(self,name,coursePreference):
		self.name = name
		self.coursePreference = coursePreference
		self.course = []
		self.crdt = 0
		self.busyMatrix = [
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False],
				[False,False,False,False,False,False,False,False]
			]
	def isFree(self,day,time,n):
		logic = True
		for i in range(0,n,1):
			logic = (not self.busyMatrix[day][time+i]) and logic
		return logic
	def setBusy(self,day,time,n):
		for i in range(0,n,1):
			self.busyMatrix[day][time+i]=True
	#assign a course to a teacher
	def add(self,course):
		#calculate the total credit hour the teacher has
		self.crdt += (course.creditHoure + course.labCredit) * course.numberOfSections
		self.course.append(course)
	
	#return the  total crdt
	def totalCredit(self):
		return self.crdt
		
	#return a my course at index i
	def myCourse(self,i):
		try:
			return self.course[i]
		except:
			return None
	#periods should not be more than 2 hours l
	# TODO
	#  [ ] design a single stone pattern for this function
	def getPeriods(self,crs=None):
		periods = []
		if crs == None:
			for i in range(0,len(self.course),1):
				number_of_periods = int(self.course[i].creditHoure/Teacher.MAX_NUMBER_OF_HOURS)
				for j in range(0,number_of_periods,1):			
					periods.append(Period(self,self.course[i],Teacher.MAX_NUMBER_OF_HOURS))
				additional = self.course[i].creditHoure%Teacher.MAX_NUMBER_OF_HOURS
				if additional > 0:
					periods.append(Period(self,self.course[i],additional))
		else:
			number_of_periods = int(crs.creditHoure/Teacher.MAX_NUMBER_OF_HOURS)
			for j in range(0,number_of_periods,1):			
				periods.append(Period(self,crs,Teacher.MAX_NUMBER_OF_HOURS))
			additional = crs.creditHoure%Teacher.MAX_NUMBER_OF_HOURS
			if additional > 0:
				periods.append(Period(self,crs,additional))
		return periods
	#rank the course according to the preference of teacher
	def rank(self, course):
		try:
			return self.coursePreference.rank.index(course)+1
		except:
			#no preference for the course have been found
			return 100
	#print teacher string
	def __str__(self):
		crs = ""
		for c in self.course:
			crs += "  "+str(c)+"  "
		return str(self.name)+" : "+str(crs)+" \n total credit hour: "+str(self.totalCredit())

#schedule course to Teacher
def schedule_seciton_to_Teacher(courses,teachers):		
	for c in courses:
		selectedTeacher = teachers[0]
		selectedTeacherScore = selectedTeacher.rank(c)+(selectedTeacher.totalCredit()+1)
		for t in teachers:
			currentTeacherScore = t.rank(c)+(t.totalCredit()+1)
			if currentTeacherScore<selectedTeacherScore:
				selectedTeacher=t
				selectedTeacherScore=currentTeacherScore
		selectedTeacher.add(c)
		c.add(selectedTeacher)
def schedule_to_class_rooms(rooms,sxns,allowedDayOftheWeek=[0,1,2,3,4]):
	leftover_section_index=-1 # the starting index of left over sections
	if len(sxns) > len(rooms):
		# there is left over sections
		for j in range(0,len(rooms),1):
			rooms[j].section.append(sxns[j])
		leftover_section_index = len(rooms) # starting index of leftovers in sxns list 
	else:
		#every section has a room
		for i in range(0,len(sxns),1):
			rooms[i].section.append(sxns[i])
	for room in rooms:
		for section in room.section:
			for course in section.courses:
				for period in course.getPeriods():
					period.section = section
					assigned = False
					for hour in range(0,8,1):
						if assigned:
							break
						for day in allowedDayOftheWeek:
							if assigned:
								break
							if (room.assign(period,day,hour)):
								assigned = True
					if(not assigned):
						print("conflict!: "+str(period))
	#check if there is a left over	
	if leftover_section_index > -1:
		for i in range(leftover_section_index,len(sxns),1):
			#rank the rooms based on the available time slot
			rooms.sort(reverse=True)
			for course in sxns[i].courses:
				for period in course.getPeriods():
					period.section=sxns[i]
					assigned = False
					for room in rooms:
						if assigned:
							break
						for hour in range(0,8,1):
							if assigned:
								break
							for day in allowedDayOftheWeek:
								if assigned:
									break
								if (sxns[i].isFreeAt(day,hour,period.length) and room.assign(period,day,hour)):
									assigned = True
									sxns[i].setBusy(day,hour,period.length)
					if(not assigned):
						print("conflict!: "+str(period))

def schedule_labs(labs,sxns,allowedDayOftheWeek=[0,1,2,3,4]):
	leftover_section_index = 0
	if len(labs) < len(sxns):
		#there is a left over sxn
		for i in range(0,len(labs),1):
			labs[i].section.append(sxns[i])
		leftover_section_index=len(labs)
	else:
		for i in range(0,len(labs)):
			labs[i].section.append(sxns[i])
	for lab in labs:
		for section in lab.section:
			for course in section.courses:
				for period in course.getLabPeriod():
					period.section = section
					assigned = False
					for hour in range(0,8,1):
						if assigned:
							break
						for day in allowedDayOftheWeek:
							if assigned:
								break
							if (lab.assign(period,day,hour)):
								assigned = True
					if(not assigned):
						print("conflict!: "+str(period))
	#check if there is a left over	
	if leftover_section_index > -1:
		for i in range(leftover_section_index,len(sxns),1):
			#rank the labs based on the available time slot
			labs.sort(reverse=True)
			for course in sxns[i].courses:
				for period in course.getLabPeriod():
					period.section=sxns[i]
					assigned = False
					for lab in labs:
						if assigned:
							break
						for hour in range(0,8,1):
							if assigned:
								break
							for day in allowedDayOftheWeek:
								if assigned:
									break
								if (sxns[i].isFreeAt(day,hour,period.length) and lab.assign(period,day,hour)):
									assigned = True
									sxns[i].setBusy(day,hour,period.length)
					if(not assigned):
						print("conflict!: "+str(period))

					

def main():
	ai =  course("AI",3,4)
	ab =  course("AB",4,8)
	ac =  course("Ac",4,4)
	ad =  course("Ad",4,4)
	ae =  course("Ae",4,4)
	af =  course("Af",4,4)
	ag =  course("ag",4,4)
	ah =  course("ah",4,4)

	taPref =  coursePreference([ae,ab,ah])
	tbPref =  coursePreference([ab,ai])
	
	ta = Teacher("ta",taPref)
	tb = Teacher("tb",tbPref)
	
	courses  = [ai,ab,ac,ad,ae,af,ag,ah]
	teachers  = [ta,tb]
	
	r1 = Room("r1")
	r2 = Room("r2")

	l1 = Room("l1")
	l2 = Room("l2")

	s1 = section("s1",1,1,[ai])
	s2 = section("s2",1,1,[ae])
	s3 = section("s3",1,1,[ae])
	s4 = section("s4",1,1,[])
	# s5 = section("s5",1,1,[ai,npmab,ac,ad])
	
	sections = [s1,s2,s3,s4]
	rooms = [r1,r2]
	labs = [l1,l2]

	schedule_seciton_to_Teacher(courses,teachers)
	schedule_to_class_rooms(rooms,sections)
	schedule_labs(labs,sections)
	
	for l in labs:
		print (l)

	for r in rooms:
		print(r)
	
	for t in teachers:
		print(str(t))
	
if __name__ == "__main__":
	main()
	
	
	