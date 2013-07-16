# -*- coding: utf-8 -*-

import unicodedata
import random

def readLines(fhandle, enc = 'utf-8'):
    for line in fhandle:
        yield line.decode(enc).strip()

def fixSeparators(line, sep = '#'):
    parts = line.split(sep)
    if len(parts) > 2:
        return ''.join(parts[:-1])+'#'+parts[-1]
    else:
        return '#'.join(parts)
 
def stripAccents(unicodeString):
    def NFD(unicodeString):
        return unicodedata.normalize('NFD', unicodeString)
    
    def isAccent(char):
        return unicodedata.category(char) == 'Mn'
    
    return ''.join((char for char in NFD(unicodeString) if not isAccent(char) ))

def convertNamesToLowercase(line):
    name, gender = line.split('#')
    return name.lower() + '#' + gender

def removeNonAlphaChars(line):
    name, gender = line.split('#')
    isValid = lambda char : char.isalpha() or char.isspace()
    name = ''.join((char for char in name if isValid(char)))
    return name + '#' + gender

def textPreProcessor(line):
    sepsFixed = fixSeparators(line.strip())
    noAccents = stripAccents(sepsFixed)
    lowercaseNames = convertNamesToLowercase(noAccents)
    alphaOnly = removeNonAlphaChars(lowercaseNames)
    return alphaOnly

def isNameEmpty(line):
    name, gender = line.split("#")
    return name.isspace()

trainProportion = 0.9

with open('sexo.csv', 'r') as dataraw, open('training.csv', 'w') as train, open('testing.csv', 'w') as test:
    for k, line in enumerate(readLines(dataraw)):
        preprocessed = textPreProcessor(line)
        if random.uniform(0,1) < trainProportion and not isNameEmpty(preprocessed):
            print >> train, preprocessed.encode('utf-8')
        elif not isNameEmpty(preprocessed):
            print >> test, preprocessed.encode('utf-8')



import pandas

data = pandas.read_csv('training.csv', sep='#', names = ["name", "gender"], index_col= None, skiprows=0)
data.head(n=10)

def shinglesn(word, n = 4):
    return [word[i:i + n].lower() for i in range(len(word) - n + 1)]

def shingles(word):
    return shinglesn(word, n=2) + shinglesn(word, n=3) + shinglesn(word, n=4) + shinglesn(word, n=5)

def firstName(name):
    try:
        return name.split()[0]
    except Exception, e:
        raise Exception(e.message + ' ' + str([name]))

def shingler(df):
    res = {'gender': [], 'name': [], 'shingle': []}
    for _, row in df.iterrows():
        name, gender = row
        for shingle in shingles(firstName(name)):
            res['gender'].append(gender)
            res['name'].append(name)
            res['shingle'].append(shingle)
    return pandas.DataFrame(res)

def countMaleFemale(df): 
    return pandas.Series({'males': df.gender[df.gender == 'M'].count(), 
                          'females': df.gender[df.gender == 'F'].count()})
 



shingleGenderCorr = data.groupby('name').apply(shingler).groupby('shingle').apply(countMaleFemale)
shingleGenderCorr.index = pandas.Series([string.decode('latin1') for string in shingleGenderCorr.index])
shingleGenderCorr.sort('females', ascending=False).head()

total = pandas.DataFrame({'total':shingleGenderCorr.males + shingleGenderCorr.females})
total.sort('total', ascending=False).head()

hist = total.groupby('total').count()
plot(log(map(float, hist.index)), log(map(float, hist.total)), '.')

alpha = 0.5
T = (shingleGenderCorr.sum()['females'] + 2 * alpha) / (shingleGenderCorr.sum()['males'] + 2* alpha)
Chi = (shingleGenderCorr.sum()['females'] + alpha) / (shingleGenderCorr.sum()['males'] + alpha)
deltas = (shingleGenderCorr.females + alpha) / (shingleGenderCorr.males + alpha)
atleds = (shingleGenderCorr.females.sum() - shingleGenderCorr.females + alpha) / (shingleGenderCorr.males.sum() - shingleGenderCorr.males + alpha)

Omega = exp(-atleds.size * log(T) + log(atleds).sum())
Theta = deltas / atleds

def getTheta(shingle):
    return Theta.get(shingle, 1.0 / Chi)

def probMale(shingles):
    const = Chi * Omega
    active = prod([getTheta(shingle) for shingle in shingles])
    return 1.0 / (1.0 + const * active)
    
probMale(shingles('mandy'))

testdata = pandas.read_csv('testing.csv', sep='#', names = ["name", "gender"], index_col= None, skiprows=0)

count = 0.0
error = 0.0
for k, row in testdata.iterrows():
    try:
        name, gender = row
        shings = shingles(firstName(name))
        sigma = -1 if gender == 'F' else 1
        score = (2.0 * probMale(shings) - 1.0) * sigma
        if score < 0.0:
            #print firstName(name), probMale(shings), gender
            error += 1.0
        count += 1.0
    except:
        pass
    if k > 100:
        break
print (count - error)/count

shingleGenderCorr.index = pandas.Series([string.encode('utf8') for string in shingleGenderCorr.index])
shingleGenderCorr.to_csv('trainingshingles.csv', sep = '#')


