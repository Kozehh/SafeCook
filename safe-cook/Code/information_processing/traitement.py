import numpy as np
from datetime import datetime


class frameData():
    def __init__(self, classNb, conf, pos):
        self.classNb = classNb
        self.conf = conf
        self.pos = pos

class DataManager():
    def __init__(self, objPath):
        self.classes = self.loadClasses(objPath)
        self.stoveIndex = self.classes.index('Stove')
        self.lastStoveFound = None

    def loadClasses(self, objPath):
        with open(objPath) as f:
            return f.read().splitlines()

    def stringToData(self, str):
        if str == '':
            return set()
        data = str[1:].split('#')
        dataSet = []
        stoveFound = False
        for d in data:
            obj = tuple(d.split('|'))
            fData = frameData(int(obj[0]), float(obj[1]), tuple((obj[2][1:-1].split(','))))
            dataSet.append(fData)
            # If the class is a stove we remember it
            if obj[0] == self.stoveIndex:
                stoveFound = True
                self.lastStoveFound = fData
        # If no even is found for this frame, we give it the last known position
        # We do this so we can remember that there is still a stove under a frying pan for example
        if not stoveFound:
            dataSet.append(self.lastStoveFound)
        return dataSet

    def findObjOverlap(self, data):
        overlapDict = {}
        for i in range(len(data)):
            for j in range(i+1, len(data)-1):
                obj1 = data[i]
                obj2 = data[j]
                # si ce n'est pas la meme classe d'objet
                if obj1.classNb != obj2.classNb:
                    if self.isRectOverlap(obj1.pos, obj2.pos):
                        # We make sure the objects have the same order
                        objs = (min(obj1.classNb, obj2.classNb), max(obj1.classNb, obj2.classNb))
                        # probability of an overlap is the prob to find the two obj where they are
                        prob = obj1.conf * obj2.conf
                        if not (objs in overlapDict):
                            overlapDict[objs] = prob
                        else:
                            overlapDict[objs] = max(prob, overlapDict[objs])
        return overlapDict

    def isRectOverlap(self, r1, r2):
        r1Corner = [int(r1[0]), int(r1[1]), int(r1[0]) + int(r1[2]), int(r1[1]) + int(r1[3])]
        r2Corner = [int(r2[0]), int(r2[1]), int(r2[0]) + int(r2[2]), int(r2[1]) + int(r2[3])]
        if (r1Corner[0] >= r2Corner[2]) or (r1Corner[2] <= r2Corner[0]) or (r1Corner[3] <= r2Corner[1]) or (r1Corner[1] >= r2Corner[3]):
            return False
        else:
            return True


    def writeOutputMsg(self, overlapDict):
        msg = str(datetime.now().time()) + " : "
        for overlap in overlapDict:
            msg += self.classes[overlap[0]] + " and " + self.classes[overlap[1]] + " are overlaping at a probability of " + str(int(overlapDict[overlap] * 100)) + "%, "
        return msg
