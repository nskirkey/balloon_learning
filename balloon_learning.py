# balloon_learning.py by Nicolas Skirkey
# 5/4/2017

import socket
import numpy
import random

def qScore(s, a):
	if(s == "1empty"):
		return empty1[a]
	elif(s == "1good"):
	    return good1[a]
	elif(s == "1bad"):
	    return bad1[a]
	elif(s == "2empty"):
	    return empty2[a]
	elif(s == "2good"):
	    return good2[a]
	elif(s == "2bad"):
	    return bad2[a]
	elif(s == "3empty"):
	    return empty3[a]
	elif(s == "3good"):
	    return good3[a]
	elif(s == "3bad"):
	    return bad3[a]
	elif(s == "4empty"):
	    return empty4[a]
	elif(s == "4good"):
	    return good4[a]
	elif(s == "4bad"):
	    return bad4[a]
	elif(s == "5empty"):
	    return empty5[a]
	elif(s == "5good"):
	    return good5[a]
	elif(s == "5bad"):
	    return bad5[a]
	elif(s == "6empty"):
	    return empty6[a]
	elif(s == "6good"):
	    return good6[a]
	elif(s == "6bad"):
	    return bad6[a]
	elif(s == "7empty"):
	    return empty7[a]
	elif(s == "7good"):
	    return good7[a]
	elif(s == "7bad"):
	    return bad7[a]

def state(s):
	if(s == "1empty"):
		return empty1
	elif(s == "1good"):
	    return good1
	elif(s == "1bad"):
	    return bad1
	elif(s == "2empty"):
	    return empty2
	elif(s == "2good"):
	    return good2
	elif(s == "2bad"):
	    return bad2
	elif(s == "3empty"):
	    return empty3
	elif(s == "3good"):
	    return good3
	elif(s == "3bad"):
	    return bad3
	elif(s == "4empty"):
	    return empty4
	elif(s == "4good"):
	    return good4
	elif(s == "4bad"):
	    return bad4
	elif(s == "5empty"):
	    return empty5
	elif(s == "5good"):
	    return good5
	elif(s == "5bad"):
	    return bad5
	elif(s == "6empty"):
	    return empty6
	elif(s == "6good"):
	    return good6
	elif(s == "6bad"):
	    return bad6
	elif(s == "7empty"):
	    return empty7
	elif(s == "7good"):
	    return good7
	elif(s == "7bad"):
	    return bad7

def getAction(a):
	if(a == 0):
		return "up"
	elif(a == 1):
		return "stay"
	elif(a == 2):
		return "down"

# Presets
iterations = 10000
discount_rate = 0.5
learning_rate = 0.1
exploration_rate = 0.8

# Arrays representing table of Q-Values initiated to 0.5
empty1 = [0.5, 0.5, 0.5]
good1 = [0.5, 0.5, 0.5]
bad1 = [0.5, 0.5, 0.5]
empty2 = [0.5, 0.5, 0.5]
good2 = [0.5, 0.5, 0.5]
bad2 = [0.5, 0.5, 0.5]
empty3 = [0.5, 0.5, 0.5]
good3 = [0.5, 0.5, 0.5]
bad3 = [0.5, 0.5, 0.5]
empty4 = [0.5, 0.5, 0.5]
good4 = [0.5, 0.5, 0.5]
bad4 = [0.5, 0.5, 0.5]
empty5 = [0.5, 0.5, 0.5]
good5 = [0.5, 0.5, 0.5]
bad5 = [0.5, 0.5, 0.5]
empty6 = [0.5, 0.5, 0.5]
good6 = [0.5, 0.5, 0.5]
bad6 = [0.5, 0.5, 0.5]
empty7 = [0.5, 0.5, 0.5]
good7 = [0.5, 0.5, 0.5]
bad7 = [0.5, 0.5, 0.5]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 24383)
sock.connect(server_address) # connect 

i = 0

data =  open("Clear_Skies_data.txt", "w")


while iterations > 0:
    if (iterations == 1000) or (iterations == 4000) or (iterations == 7000):
        exploration_rate = exploration_rate * exploration_rate

    # Response from server
    d = sock.recv(1024).strip() # need the receive in order to send separate messages
    print "Iteration: ", iterations
    print "Received:", d        # (blocking socket)    
    
    
    response = d.split(",")
    s = state(response[0])
    a = response[1]
    r = float(response[2])
    ns = state(response[3])

    if a == "up":
        action = 0
    if a == "stay":
        action = 1
    if a == "down":
        action = 2

    # Update q-score
    s[action] = (1.0 - learning_rate)*qScore(response[0],action)+learning_rate*(r+discount_rate*numpy.amax(ns))
    new_action = ""
    
    # Explore with probability of exploration_rate
    explore = (numpy.random.random() < exploration_rate)

    # Explore or stick to policy
    if explore == 1:
        random_action = random.randint(0, 2)
        if(random_action == 0):
            new_action = "up"
        elif(random_action == 1):
            new_action = "stay"
        elif(random_action == 2):
            new_action = "down"
    else:
        new_action = getAction(ns.index(numpy.amax(ns)))


    print "New action: ", new_action
    print "Exploration rate: ", exploration_rate
    # Send new action 
    sock.sendall(new_action)
    iterations -= 1

# Write final q-values to file
data.write("Final Q-values:\n" +
		"       up  stay  down\n"
		"empty1: " + " ".join(str(n) for n in empty1) + "\n" +
		"good1: " + " ".join(str(n) for n in good1) + "\n" +
		"bad1: " + " ".join( str(n) for n in bad1) + "\n"
		"empty2: " + " ".join( str(n) for n in empty2) + "\n"
		"good2: " + " ".join( str(n) for n in good2) + "\n"
		"bad2: " + " ".join( str(n) for n in bad2) + "\n"
		"empty3: " + " ".join( str(n) for n in empty3) + "\n"
		"good3: " + " ".join( str(n) for n in good3) + "\n"
		"bad3: " + " ".join( str(n) for n in bad3) + "\n"
		"empy4: " + " ".join( str(n) for n in empty4) + "\n"
		"good4: " + " ".join( str(n) for n in good4) + "\n"
		"bad4: " + " ".join( str(n) for n in bad4) + "\n"
		"empty5: " + " ".join( str(n) for n in empty5) + "\n"
		"good5: " + " ".join( str(n) for n in good5) + "\n"
		"bad5: " + " ".join( str(n) for n in bad5) + "\n"
		"empty6: " + " ".join( str(n) for n in empty6) + "\n"
		"good6: " + " ".join( str(n) for n in good6) + "\n"
		"bad6: " + " ".join( str(n) for n in bad6) + "\n"
		"empty7: " + " ".join( str(n) for n in empty7) + "\n"
		"good7: " + " ".join( str(n) for n in good7) + "\n"
		"bad7: " + " ".join( str(n) for n in bad7) + "\n"
)
