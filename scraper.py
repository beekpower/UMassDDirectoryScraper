from bs4 import BeautifulSoup
from array import *
import urllib2
import csv
#open CSV file for output
with open('directory.csv', 'w') as csvfile:
    # Write column headers as the first line
    fieldnames = ['First Name', "Last Name", 'Title', 'Department', 'Building', 'Room', 'Employment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    #Keeps track of the number of all directory entries for last name letter category
    linkNum = 0
    #Keeps track of the number of faculty directory entries for last name letter category
    facultyNum = 0
    #Index used for traversing through the list of faculty entries in the directory 
    facultyIndex = 1
    #Keeps track of the number of staff directory entries for last name letter category
    staffNum = 0
    #Index used for traversing through the list of staff entries in the directory 
    staffIndex = 1
    #Array of each letter in the alphabet with the exception of 'U' (there are currently not entries for last names that begin with 'U'
    alphabetArray = array('c',['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'])
    
    #Loop through list of directory entries by first letter of last name
    for i in alphabetArray:
        linkNum = 0
        facultyNum = 0
        facultyIndex = 1
        staffNum = 0
        staffIndex = 1
        
        #read UMassD Online Directory
        file = urllib2.urlopen("http://www1.umassd.edu/directory/welcome.cfm?fl="+i+"&sclm=n&pa=")
        html = file.read()
        file.close()
        
         #read UMassD Online Faculty Directory
        facultyFile = urllib2.urlopen("http://www1.umassd.edu/directory/welcome.cfm?f=&q=&fl="+i+"&sclm=n&pa=faculty")
        facultyHtml = facultyFile.read()
        facultyFile.close()
            
         #read UMassD Online Staff Directory
        staffFile = urllib2.urlopen("http://www1.umassd.edu/directory/welcome.cfm?f=&q=&fl="+i+"&sclm=n&pa=staff")
        staffHtml = staffFile.read()
        staffFile.close()

        #Use BeautifulSoup to help find how many entries are in each category list
        soup = BeautifulSoup(html, 'lxml')
        for table in soup.findAll('table')[1:]:     #find second table...
            for tr in table.findAll('tr')[1:]:      #...then the rows after the first one in the table...
                for td in tr.findAll('td'):         #... then the data in the table tow...
                    for font in td.findAll('a'):    #... and finally the link of the professors name
                        linkNum+=1
        #Use BeautifulSoup to help find how many faculty entries are in each category list            
        facultySoup = BeautifulSoup(facultyHtml, 'lxml')
        for table in facultySoup.findAll('table')[1:]:     #find second table...
            for tr in table.findAll('tr')[1:]:      #...then the rows after the first one in the table...
                for td in tr.findAll('td'):         #... then the data in the table tow...
                    for font in td.findAll('a'):    #... and finally the link of the professors name
                        facultyNum+=1
        #Use BeautifulSoup to help find how many staff entries are in each category list
        staffSoup = BeautifulSoup(staffHtml, 'lxml')
        for table in staffSoup.findAll('table')[1:]:     #find second table...
            for tr in table.findAll('tr')[1:]:      #...then the rows after the first one in the table...
                for td in tr.findAll('td'):         #... then the data in the table tow...
                    for font in td.findAll('a'):    #... and finally the link of the professors name
                        staffNum+=1

        #Loop through all entries and pull information from it (Name, Title, Department, Building, Room)
        for x in range(1, linkNum+1):
            #open detailed information for professor link
            file2 = urllib2.urlopen("http://www1.umassd.edu/directory/welcome.cfm?f=&rn="+str(x)+"&q=&fl="+i+"&sclm=n&pa=#"+str(x))
            html2 = file2.read()
            file2.close()

            #Use BeautifulSoup to find the tags where the desired information is located
            soup2 = BeautifulSoup(html2, 'lxml')
            name = soup2.findAll('table')[1].findAll('tr')[x+1].findAll('td')[0].findAll('font')[0].text.strip()
            title = soup2.findAll('table')[1].findAll('tr')[x+1].findAll('td')[0].findAll('font')[1].text.strip()
            department = soup2.findAll('table')[1].findAll('tr')[x+1].findAll('td')[1].findAll('font')[0].text.strip()
            location = soup2.findAll('table')[1].findAll('tr')[x+1].findAll('td')[1].findAll('font')[1].text.strip()
            employment = ''
            #compare directory entries with faculty and staff entries to determine the employment status of the current entry 
            if facultyIndex <= facultyNum and name == facultySoup.findAll('table')[1].findAll('tr')[facultyIndex].findAll('td')[0].findAll('font')[0].text.strip():
                facultyIndex += 1
                employment = 'F'
            if staffIndex <= staffNum and name == staffSoup.findAll('table')[1].findAll('tr')[staffIndex].findAll('td')[0].findAll('font')[0].text.strip():
                staffIndex += 1
                employment = 'S'
            #print name + " " + title + " " + department + " " + location + " " + employment
            #encode strings to UTF-8 so that the results can output in CSV format
            write_fname = u''.join(name.split(", ")[1]).encode('utf-8')
            write_lname = u''.join(name.split(", ")[0]).encode('utf-8')
            write_title = u''.join(title).encode('utf-8')
            write_department = u''.join(department).encode('utf-8')
            #check if room number is defined
            if "Room" not in location:
                write_building = u''.join(location).encode('utf-8')
                write_room = u''.join("").encode('utf-8')
            else:
                write_building = u''.join(location.split(", Room: ")[0]).encode('utf-8')
                write_room = u''.join(location.split(", Room: ")[1]).encode('utf-8')
            if employment:
                write_employment = u''.join(employment).encode('utf-8')
            else:
                write_employment = u''.join("").encode('utf-8')

            #write results in CSV file
            writer.writerow({'First Name': write_fname, 'Last Name': write_lname, 'Title': write_title, 'Department': write_department, 'Building': write_building, 'Room': write_room, 'Employment': write_employment})
