from flask import Flask, render_template, request
from werkzeug import secure_filename
import csv
import datetime 


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
	

	list_of_dates = {}
	all_students = []
	weekly = (2019, 5, 1)
	class Student:
		def __init__(self):
			self.lastname = 'lastname'	
			self.firstname = 'firstname'
			self.timestamp = 'timestamp'
			self.unavailable_dates = []
	
	with open(f.filename) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
	
		for row in readCSV:
			stu = Student()
			stu.firstname = row[1]
			stu.lastname = row[2]
			row_3 = row[3].split(";")
			for item in row_3:
				if item == "Monday":
					stu.unavailable_dates.append(datetime.date(int(weekly[0]), int(weekly[1]), int(weekly[2])))
				if item == "Tuesday":
					stu.unavailable_dates.append(datetime.date(int(weekly[0]), int(weekly[1]), int(weekly[2])+1))
				if item == "Wednsday":
					stu.unavailable_dates.append(datetime.date(int(weekly[0]), int(weekly[1]), int(weekly[2])+2))
				if item == "Thursday":
					stu.unavailable_dates.append(datetime.date(int(weekly[0]), int(weekly[1]), int(weekly[2])+3))
				if item == "Friday":
					stu.unavailable_dates.append(datetime.date(int(weekly[0]), int(weekly[1]), int(weekly[2])+4))
			holder = [stu.firstname, stu.lastname, stu.unavailable_dates]
			all_students.append(holder)



	def daterange(start_date, end_date):
		for n in range(int ((end_date - start_date).days)):
			yield start_date + datetime.timedelta(n)

	start_date = datetime.date(weekly[0], weekly[1], weekly[2])
	end_date = datetime.date(weekly[0], weekly[1], weekly[2]+7)
	for single_date in daterange(start_date, end_date):
		placeholder_list = []
		for student in all_students:
			check = 0

			if len(student[2]) != 0:
				for item in student[2]:
					if item == single_date:
					
						check = 1
			if check == 0:
				placeholder_list.append(student[1])

		

		list_of_dates[single_date] = placeholder_list


	newlist = []
	pretty_list = []
	for i in range(0, 7):
		for item in list_of_dates:
			if item == start_date:
				pretty_list.append(item)
			start_date = datetime.date(weekly[0], weekly[1], weekly[2] + i)



	print ("Available Dates:")
	for item in pretty_list:
		newlist.append("\n")
		newlist.append(str(item))
		people = list_of_dates[item]
		for person in people:
		
			newlist.append(person)

	str1 = ', '.join(newlist)
	return(str1)

	#return pretty_list

if __name__ == '__main__':
	app.run(debug=True)

