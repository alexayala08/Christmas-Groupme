import json
import os
import operator
from collections import Counter

#global variables because I'm lazy and didn't feel like thinking
#of a more elegant solution
total_messages = 0
liked_messages = 0
likes_received = 0
biggest_fans = {}
all_words = {}
most_liked_message_num = 0
most_liked_message = []
#poi = person of interest
poi = ""
temp = 0



def check_group(group, person):
    global total_messages
    global liked_messages
    global likes_received
    global all_words
    global biggest_fans
    global most_liked_message_num
    global most_liked_message

    #common words and contractions that are ignored when
    #looking for unique words
    temp_words = "THE BE TO OF AND A IN THAT HAVE I IT FOR NOT ON WITH HE AS \
    YOU DO AT THIS BUT HIS BY FROM THEY WE SAY HER SHE OR AN WILL MY ONE ALL \
    WOULD THERE THEIR WHAT SO UP OUT IF ABOUT WHO GET WHICH GO ME WHEN MAKE \
    CAN LIKE TIME NO JUST HIM KNOW TAKE PEOPLE INTO YEAR YOUR GOOD SOME COULD \
    THEM SEE OTHER THAN THEN NOW LOOK ONLY COME ITS OVER THINK ALSO BACK AFTER \
    USE TWO HOW OUR WORK FIRST WELL WAY EVEN NEW WANT BECAUSE ANY THESE GIVE \
    DAY MOST US IS ARE I'M WAS DON'T I'LL I’M DON’T I’LL IT'S IT’S THAT'S \
    THAT’S WE'RE WE’RE YOU'RE YOU’RE"
    common = temp_words.split()

    #opens groupchat file with all of the groups messages
    path = os.getcwd() + "\\"+group
    with open(path+'\\message.json', encoding="utf8") as f:
        data = json.load(f)

    #Reads through all message to collect data on poi
    for message in range(len(data)):

        #Tracks which messages from poi have been liked and most liked
        if(data[message]["user_id"]) == person:
            total_messages += 1
            if(len(data[message]["favorited_by"]) > 0):
                liked_messages += 1
                if (len(data[message]["favorited_by"]) > most_liked_message_num):
                    most_liked_message_num = len(data[message]["favorited_by"])
                    most_liked_message = data[message]["text"]
            likes_received += len(data[message]["favorited_by"])

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




#loop to check all group chats
def check_all_groups(person):
    for folder in os.listdir():
        if folder == 'Christmas.py':
            break
        check_group(folder, person)

#Asks user who they want information on
def take_input():
    global poi

    yourself = input("Do you want to learn about yourself? (y/n): ")   
    while yourself.upper() != 'Y' and yourself.upper() != 'N':
        yourself = input("Sorry I didn't understand that. Do you want to learn about yourself? (y/n): ")

    if(yourself.upper() ==  'Y'):
        profile = os.getcwd() + "\\profile\\profile.json"
        with open(profile, encoding="utf8") as f:
            data = json.load(f)
        person = (data['id'])
        poi = (data["name"])
        poi = poi.split()
        return person

    elif(yourself.upper() == 'N'):
        temp = input("Who would you like to learn about? (Case Sensitive): ")
        person = find_person_id(temp)
        poi = temp.split()
        while person == None:
            print("Sorry it seems we could not find that person")
            temp = input("Who would you like to learn about? (Case Sensitive): ")
            person = find_person_id(temp)
            poi = temp
        return person

#Prints out the collected data
def statistics():
    global total_messages
    global liked_messages
    global likes_received
    global all_words
    global biggest_fans
    global most_liked_message_num
    global most_liked_message

    print()
    print("Total number of messages", poi[0], "has sent:", total_messages)
    print("Total number of likes", poi[0], "has received:",likes_received)
    print("Average likes per message for", poi[0], ":", round(likes_received/total_messages, 3))

    print() 
    print("Messages that received at least one like:", liked_messages)
    print("Improved LPM using messages with at least one like:", round(likes_received/liked_messages,3))

    print()
    print("Improved LPM vs normal LPM:", round(likes_received/liked_messages - likes_received/total_messages, 3))
    print("This number represents how many more likes a person will receive when actually trying \
to receive likes")

    print()
    print(most_liked_message_num)
    print(most_liked_message)

    #sorts biggest fans and returns top 10
    f = Counter(biggest_fans)
    fans = f.most_common(10)
    print()
    print("The people that have given", poi[0], "the most likes: ", end = "")
    for f in fans:
        print(find_person_name(f[0]), f[1] , end = ", ")
    print()

    #sorts words by how often they are used and returns top 10
    common_words = {}
    k = Counter(all_words)
    high = k.most_common(10)
    print()
    print("Some unique words", poi[0], "has said often: ", end ="")
    for i in high:
        print(i[0], i[1] , end = ", ")
    print()

def final():
    global total_messages
    global liked_messages
    global likes_received
    global biggest_fans
    global all_words
    
    person = take_input()
    check_all_groups(person)
    statistics()
    print()
    again = input("Do you want to learn about someone else? (y/n): ")
    while again.upper() == 'Y':
        total_messages = 0
        liked_messages = 0
        likes_received = 0
        biggest_fans = {}
        all_words = {}
        most_liked_message_num = 0
        most_liked_message = []
        
        person = take_input()
        check_all_groups(person)
        statistics()
        print()
        again = input("Do you want to learn about someone else? (y/n): ")

final()

