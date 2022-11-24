import json
import os 
import time
import math
import sys
import re
from send2trash import send2trash

THIS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
defaultRules = None
option = "" if len(sys.argv) < 2 else sys.argv[1]

def main():
    global defaultRules
    print("========== Start ==========")
    if(option != "del"):
        print("Add argument \"del\" to actually delete files")

    settings = getSettings()
    defaultRules = settings["defaultRules"]
    for folderItem in settings["folders"]:
        deleteOldFiles(folderItem)



def getSettings():
    global settings

    settingsPath = THIS_DIRECTORY + os.sep + "settings.json"
    file = open(settingsPath)
    return json.load(file)


def deleteOldFiles(folderItem):
    for itemName in os.listdir(folderItem["path"]):
        itemPath = folderItem["path"] + os.sep + itemName
        itemAge = getItemAge(itemPath)
        rule = getFirstMatchingRule(folderItem["rules"], itemPath)

        if rule is None:
            continue
        if itemAge >= rule["deleteAfterDays"]:
            deleteItem(itemPath)


def getItemAge(path):
    lastModified = os.path.getmtime(path)
    ageInSeconds = time.time() - lastModified
    ageInDays = ageInSeconds / 3600 / 24
    return math.floor(ageInDays)


def getFirstMatchingRule(rulesForFolder, itemPath):
    rules = rulesForFolder + defaultRules
    for rule in rules:
        ruleMatches = doesRuleMatch(rule["pattern"], itemPath)
        if(ruleMatches):
            return rule


def doesRuleMatch(rulePattern, itemPath):
    if(rulePattern == "<folder>"):
        return os.path.isdir(itemPath)
    if(re.match(rulePattern, itemPath)):
        return True
    return False


def deleteItem(path):
    if(option == "del"):
        try:
            send2trash(path)
            print("Deleted: ", path)
        except OSError:
            print("Could not delete ", path)
    else:
        print("Would have deleted: ", path)

main()