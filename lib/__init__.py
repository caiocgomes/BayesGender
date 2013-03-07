import csv
import os.path

resourcedir = os.path.join(os.path.dirname(__file__), '../res')
countFile = open(os.path.join(resourcedir, 'namesGenderFrequencyFile.txt'), 'r')
data = {name:(float(countMale), float(countFemale))
        for _, name, countMale, countFemale in csv.reader(countFile, delimiter = '|')}

totalMale, totalFemale = map(sum, zip(*data.values()))
numNames = len(data.keys())


def likelihood(gender, name, alpha = 0.5):
    countMale, countFemale = data.get(name, (0.0, 0.0))
    count = countMale if gender == 'male' else countFemale
    total = totalMale if gender == 'male' else totalFemale
    return float(count + alpha) / float(total + numNames * alpha)

def prior(gender, alpha = 0.5):
    total = totalMale if gender == 'male' else totalFemale
    return float(total + alpha) / float(totalMale + totalFemale + 2 * alpha)

def probMale(name, alpha = 0.5):
    likelyMale = likelihood('male', name, alpha = alpha)
    likelyFemale = likelihood('female', name, alpha = alpha)
    priorMale = prior('male', alpha = alpha)
    priorFemale = prior('female', alpha = alpha)
    return float(likelyMale * priorMale )/ float(likelyMale * priorMale + likelyFemale * priorFemale)
