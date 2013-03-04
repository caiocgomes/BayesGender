import csv
import os.path

resourcedir = os.path.join(os.path.dirname(__file__), '../res')
countFile = open(os.path.join(resourcedir, 'namesGenderFrequencyFile.txt'), 'r')
data = {name:(float(countMale), float(countFemale))
        for _, name, countMale, countFemale in csv.reader(countFile, delimiter = '|')}

totalMale, totalFemale = map(sum, zip(*data.values()))
numNames = len(data.keys())


def likelihood(gender, name, alpha = 0.5):
    countMale, countFemale = data[name]
    count = countMale if gender == 'male' else countFemale
    total = totalMale if gender == 'male' else totalFemale
    return (count + alpha) / (total + numNames * alpha)

def prior(gender, alpha = 0.5):
    total = totalMale if gender == 'male' else totalFemale
    return (total + alpha) / (totalMale + totalFemale + 2 * alpha)

def probMale(name, alpha = 0.5):
    likelyMale = likelihood('male', name, alpha = alpha)
    likelyFemale = likelihood('female', name, alpha = alpha)
    priorMale = prior('male', alpha = alpha)
    priorFemale = prior('female', alpha = alpha)
    return likelyMale * priorMale / (likelyMale * priorMale + likelyFemale * priorFemale)
