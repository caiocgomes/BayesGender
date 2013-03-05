from lib import probMale

def probFemale(name, alpha = 0.5):
    return 1.0 - probMale(name, alpha = alpha)
