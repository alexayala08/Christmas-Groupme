import json
import os
import operator
import sys
from collections import Counter

def check_groups(person):
    total_messages = 0
    liked_messages = 0
    likes_received = 0
    biggest_fans = {}
    all_words = {}
    most_liked_message_num = 0
    most_liked_message = []
    group_lpm = {}
    common_words = "THE BE TO OF AND A IN THAT HAVE I IT FOR NOT ON WITH HE AS \
            YOU DO AT THIS BUT HIS BY FROM THEY WE SAY HER SHE OR AN WILL MY ONE ALL \
            WOULD THERE THEIR WHAT SO UP OUT IF ABOUT WHO GET WHICH GO ME WHEN MAKE \
            CAN LIKE TIME NO JUST HIM KNOW TAKE PEOPLE INTO YEAR YOUR GOOD SOME COULD \
            THEM SEE OTHER THAN THEN NOW LOOK ONLY COME ITS OVER THINK ALSO BACK AFTER \
            USE TWO HOW OUR WORK FIRST WELL WAY EVEN NEW WANT BECAUSE ANY THESE GIVE \
            DAY MOST US IS ARE I'M WAS DON'T I'LL I’M DON’T I’LL IT'S IT’S THAT'S \
            THAT’S WE'RE WE’RE YOU'RE YOU’RE"
    common = common_words.split()
    mentions = {}
    
    for folder in os.listdir():
        try:
            int(folder)
            #opens groupchat file with all of the groups messages
            path = os.getcwd() + "\\"+folder
            with open(path+'\\message.json', encoding="utf8") as f:
                data = json.load(f)

            current_messages = 0
            current_likes = 0
            
            #Reads through all message to collect data on poi
            for message in range(len(data)):

                #Tracks stats about messages sent from poi
                if(data[message]["user_id"]) == person:
                    total_messages += 1
                    current_messages += 1
                    
                    #checks messages that have been liked
                    if(len(data[message]["favorited_by"]) > 0):
                        liked_messages += 1
                        likes_received += len(data[message]["favorited_by"])
                        current_likes += len(data[message]["favorited_by"])

                        if (len(data[message]["favorited_by"]) > most_liked_message_num):
                            most_liked_message_num = len(data[message]["favorited_by"])
                            most_liked_message = data[message]["text"]
                            
                    if(len(data[message]["attachments"]) > 0):
                        for i in range(len(data[message]["attachments"])):
                            if(data[message]["attachments"][i]["type"] == "mentions"):
                                for k in data[message]["attachments"][i]["user_ids"]:
                                    if k in mentions:
                                        mentions[k] = mentions[k] + 1
                                    else:
                                        mentions[k] = 1
                    
                    
                    #Tracks who likes poi's messages the most
                    for j in data[message]["favorited_by"]:
                        if j in biggest_fans:
                            biggest_fans[j] = biggest_fans[j] + 1
                        else:
                            biggest_fans[j] = 1

                    #Checks every word poi has ever sent
                    if data[message]["text"] != None:
                        sentence = data[message]["text"].split()
                        for word in sentence:
                            if word.upper() in common:
                                continue
                            elif word.upper() in all_words:
                                all_words[word.upper()] = all_words[word.upper()] + 1
                            else:
                                all_words[word.upper()] = 1
                                
            with open(path+'\\conversation.json', encoding="utf8") as f:
                data = json.load(f)
            if (current_messages > 0):
                group_lpm[data["name"]] = round(current_likes/current_messages, 3)
        except(ValueError):
            continue
    common_words = {}
    k = Counter(all_words)
    high = k.most_common(5)

    f = Counter(biggest_fans)
    fans = f.most_common(5)

    m = Counter(group_lpm)
    highest_lpm = m.most_common(5)

    p = Counter(mentions)
    most_mentioned = p.most_common(5)

    return total_messages, liked_messages, likes_received, high, fans, \
           most_liked_message_num, most_liked_message, highest_lpm, most_mentioned

    
#goes through each groupchat until poi's name is found
#returns poi's unique ID
def find_person_id(name):
    for folder in os.listdir():
        if folder == 'Christmas.py':
            break
        path = os.getcwd() + "\\"+folder
        with open(path+'\\conversation.json', encoding="utf8") as f:
            data = json.load(f)
        for people in range(len(data["members"])):
            if data["members"][people]["name"] == name:
                return data["members"][people]["user_id"]
            

#goes through each groupchat until poi's unique ID is found
#returns poi's Name
def find_person_name(uid):
    for folder in os.listdir():
        if folder == 'Christmas.py':
            break
        path = os.getcwd() + "\\"+folder
        with open(path+'\\conversation.json', encoding="utf8") as f:
            data = json.load(f)
        for people in range(len(data["members"])):
            if data["members"][people]["user_id"] == uid:
                return data["members"][people]["name"]


#Asks user who they want information on
def take_input():
    #global poi

    yourself = input("Do you want to learn about yourself? (y/n): ")   
    while yourself.upper() != 'Y' and yourself.upper() != 'N':
        yourself = input("Sorry I didn't understand that. Do you want to learn about yourself? (y/n): ")

    if(yourself.upper() ==  'Y'):
        profile = os.getcwd() + "\\profile\\profile.json"
        with open(profile, encoding="utf8") as f:
            data = json.load(f)
        person_id = (data['id'])
        name = (data["name"])
        name = name.split()
        return person_id, name

    elif(yourself.upper() == 'N'):
        name = input("Who would you like to learn about? (Full Name - Case Sensitive): ")
        person_id = find_person_id(name)
        name = name.split()
        while name == None:
            print("Sorry it seems we could not find that person")
            name = input("Who would you like to learn about? (Fulle Name - Case Sensitive): ")
            person_id = find_person_id(name)
            name = name.split
        return person_id, name

#Prints out the collected data
def statistics(name, total_messages, liked_messages, likes_received, high, \
               fans, most_liked_message_num, most_liked_message, highest_lpm, most_mentioned):
    print()
    print("Total number of messages", name, "has sent:", total_messages)
    print("Total number of likes", name, "has received:",likes_received)
    print("Average likes per message: ", round(likes_received/total_messages, 3))

    print() 
    print("Messages that received at least one like:", liked_messages)
    print("Improved LPM using messages with at least one like:", round(likes_received/liked_messages,3))

    print()
    print("Improved LPM - normal LPM:", round(likes_received/liked_messages - likes_received/total_messages, 3))
    print("This number represents how many more likes a person will receive when actually trying \
to receive likes")

    print()
    print(name, "overall most liked message:", most_liked_message)
    print("Likes received", most_liked_message_num)

    print()
    print("The groups where", name, "has the highest LPM:", highest_lpm)

    print()
    print("The people", name, "has mentioned the most: ", end = "")
    for m in most_mentioned:
        print(find_person_name(m[0]), m[1] , end = ", ")
    print()
    print()
    print("The people that have given", name, "the most likes: ", end = "")
    for f in fans:
        print(find_person_name(f[0]), f[1] , end = ", ")

    #sorts words by how often they are used and returns top 10
    print()
    print()
    print("Some unique words", name, "has said often: ", end ="")
    for i in high:
        print(i[0], i[1] , end = ", ")
    print()

def final():
    again = 'Y'
    while again.upper() == 'Y':
        person_id, name = take_input()
        total_messages, liked_messages, likes_received, high, \
               fans, most_liked_message_num, most_liked_message, highest_lpm, most_mentioned = check_groups(person_id)

        statistics(name[0], total_messages, liked_messages, likes_received, high, \
               fans, most_liked_message_num, most_liked_message, highest_lpm, most_mentioned)
        print()
        again = input("Do you want to learn about someone else? (y/n): ")
    print()

final()

