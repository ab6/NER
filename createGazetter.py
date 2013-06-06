

f = open("WikiPeopleRedirects.lst", 'r')
g = open("Gazetteer.txt", 'a')
className = "PEOPLE"

for line in f:
	g.write(className + " " + line)
	
f.close()
g.close()