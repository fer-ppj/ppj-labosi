import argparse #http://docs.python.org/library/argparse.html#module-argparse
import random #http://docs.python.org/library/random.html#module-random
import string #http://docs.python.org/library/stdtypes.html#string-methods
import os #http://docs.python.org/library/os.html#os.listdir
import urlparse
import csv #http://docs.python.org/library/csv.html

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler #http://docs.python.org/library/basehttpserver.html#BaseHTTPServer.BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

def readCSV(filename, keys):
  if os.path.isfile(filename):
    csvfile = open(filename, 'r')
    csvreader = csv.DictReader(csvfile, fieldnames=keys, delimiter=';', quotechar='|')
    retVal = {}
    for row in csvreader:
      retVal[row['jmbag']] = row;
    csvfile.close
    return retVal
  else:
    return None

def writeCSV(filename, keys, elems):
  csvfile = open(filename, 'w')
  writer = csv.DictWriter(csvfile, fieldnames=keys, delimiter=';', quotechar='|')
  for elem in elems:
    writer.writerow(elem)
  csvfile.close()
  return
    
def Generate():
  ppjstud = readCSV("grupe_studenti.csv", ['ime', 'prezime', 'jmbag', 'email'])
  ppjprijave = readCSV("grupe_prijave.csv", ['jmbag', 'voditelj', 'grupa']) 
  
  maxcoord = 36
  grupe = [ [] for i in range(maxcoord)]
  nerasp = []
  maxgrupa = 6
  
  for studppj in ppjstud:
    if (ppjstud[studppj]['jmbag'] in ppjprijave):
      ppjstud[studppj]['voditelj'] = ppjprijave[studppj]['voditelj']
      ppjstud[studppj]['grupa'] = ppjprijave[studppj]['grupa']
      grupe[int(ppjprijave[studppj]['grupa']) - 1].append(ppjstud[studppj])
      print("nasao studenta s grupom:" + str(ppjstud[studppj]['grupa']))
    else:
      nerasp.append(ppjstud[studppj])
      print("nasao studenta bez grupe")
  
  for neraspstud in nerasp:
    mingrupa = grupe[0]
    for grupa in grupe:
      if len(grupa) < len(mingrupa):
        mingrupa = grupa
    
    neraspstud['grupa'] = mingrupa[0]['grupa']
    neraspstud['voditelj'] = '0'
    mingrupa.append(neraspstud)
  
  rezultat = []
  for grupa in grupe:
    rezultat += grupa
  
  for i in range(maxcoord):
    print("Grupa %s ima %s clanova." %(grupe[i][0]['grupa'], str(len(grupe[i]))))
  
  writeCSV("grupe_konacno.csv", ['grupa', 'jmbag', 'voditelj', 'ime', 'prezime', 'email'], rezultat)
  return


def main():
  Generate()
  return

if __name__ == "__main__":
  main()
