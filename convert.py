import pandas as pd
import io
import os
#import csv

dict_from_csv = pd.read_csv('rezepte-small.csv', header=0, index_col=0, squeeze=True).to_dict()

def saveHtml(name, htmlCode):
    htmlCode = str("---\ntitle: " + dict_from_csv["title"][int(name)]
                   + "\n---\n\n<head>\n<meta charset=\"UTF-8\">\n</head>\n"
                   + htmlCode)
    try:
        os.mkdir("./html/" + str(name))
    except:
        print("Could not create subdirectory")
    if type(name) == int:
        with io.open(str("./html/" + str(name) + "/" + "default" + ".md"), "w", encoding="utf8") as f:
            f.write(htmlCode)
        f.close
        print("successfully saved: " + str("./html/" + str(name) + "/" + "default" + ".md"))
    else:
        with io.open(str("./html/" + str(name) + ".html"), "w", encoding="utf8") as f:
            f.write(htmlCode)
        f.close
        print("successfully saved: " + str("./html/" + str(name) + ".html"))


def createHomepage():
    homepage = "<h1>Recipes</h1>\n<table>"
    for i in range(0, len(dict_from_csv["title"]), 2):
        numberEven = i
        try:
            numberOdd = int(i + 1)
            titleOdd = dict_from_csv["title"][numberOdd]
        except:
            print("end of array reached. Cannot print nonexistent things!")
        titleEven = dict_from_csv["title"][numberEven]
        if numberOdd <= len(dict_from_csv["title"]):
            try:
                homepage = homepage + "<tr>\n" \
                              "<th><a href=\"recipes/" + str(numberEven) + "\">" + str(titleEven) + "</a>" \
                                                                                                            "</th>\n" \
                              "<th><a href=\"recipes/" + str(numberOdd) + "\">" + str(titleOdd) + "</a>" \
                                                                                                                "</th>\n" \
                                                                                                                "</tr>\n"
            except:
                print("error while generating homepage parts")
        else:
            homepage = homepage + "</table>"
        if numberEven == len(dict_from_csv["title"]) - 1:
            try:
                saveHtml("index", homepage)
            except:
                print("error while generating homepage")


def convertToHtml(int,final):
    title = dict_from_csv["title"][int] # text
    ingredients = dict_from_csv["ingredients"][int].split("\"") # array
    directions = dict_from_csv["directions"][int].split("\"") # array
    link = dict_from_csv["link"][int] # text
    source = dict_from_csv["source"][int] # text
    NER = dict_from_csv["NER"][int] # ingredients, array
    htmlfile = "<h1>" + title + "</h1>\n"
    htmlfile = htmlfile +  "<a href=\"http://"+ link + "/\">Click here for the original source</a>\n"
    htmlfile = htmlfile + "<h2>Ingredients</h2>\n"
    for i in ingredients:
         htmlfile = htmlfile + "<p>" + i.strip(",[]") + "</p>\n"
    htmlfile = htmlfile + "<h2>Directions</h2>\n\n"
    for i in directions:
        htmlfile = htmlfile + "<p>" + i.strip(",[]") + "</p>\n"

    saveHtml(str(int), htmlfile)
    if final == 1:
        createHomepage()
    # print (str(int) + title + ingredients + directions + link + source + NER)


length = len(dict_from_csv["title"])

for _ in range(length):
    if int(_) == int(length) - 1:
        try:
            convertToHtml(int(_), 1)
        except:
            print("error during last generation")
            createHomepage()
    try:
        convertToHtml(int(_), 0)
    except:
        print("There was an error in row " + str(_))



#  -------- write dictionary to csv for debug -------
# define a dictionary with key value pairs
#dict = dict_from_csv
# open file for writing, "w" is writing
#w = csv.writer(open("output.csv", "w"))
# loop over dictionary keys and values
#for key, val in dict.items():
    # write every key and value to file
#    w.writerow([key, val])