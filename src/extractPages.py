#This file takes the file consisting of all the pages of wikipedia and returns a list of all files, each containing asingle page of
#the dataset

#/personal/Wiki/enwiki-latest-pages-articles.xml"

count=0

#open file
with open("H:\MS\Web Mining\Assignment\Assignment 4\Data\sample.xml","r") as inputFile:
        for line in inputFile:
                pageData=[]
                #extract each page
                if "<page>" in line:
                        count+=1
                        while "</page>" not in line:
                                pageData.append(line)
                                line=inputFile.next()
                        pageData.append(line)

                        #write into file
                        name="H:\MS\Web Mining\Assignment\Assignment 4\Data\Sample Extracted Pages\page"+str(count)+".xml"
                        pageFile=open(name,"w")
                        pageFile.write("".join(pageData))
                        pageFile.close()
inputFile.close()

print count
