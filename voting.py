import mysql.connector as connection
mydb = connection.connect(host="127.0.0.1", user="root", password="A1482004Sodeeq", database="voting")
mycursor = mydb.cursor()


import time
import string
import random

    # Creating the Database
# mycursor.execute("CREATE DATABASE IF NOT EXISTS voting")
# mycursor.execute("use voting")

    # Creating the tables
# mycursor.execute("create table students(ID int primary key auto_increment, fname char(20), lname char(20), voteID varchar(16), password varchar(20), gender char(10), department char(20), voted char(5))")

# mycursor.execute("create table votes(ID int primary key auto_increment, voterID varchar(16), department char(20), president char(20), vicepresident char(20))")

class INEC:
    def __init__(self):
        self.candidate = ["Vote for President", "Vote for Vice President"]
        self.options = ["A: Peter Gregory Obi B: Ahmed Bola Tinubu", "A: Atiku Abubakar B: Yemi Osinbajo"]
        mydb.commit()
        self.start()
        
    def start(self):
        action = input("""
              Welcome to the VOTING platform
              ENTER 1 to login
              ENTER 2 to register 
              """)
        if action == "1": 
            self.login() 
        elif action == "2":
            self.register()
        else: 
            print("Wrong Input, try again \n")
            time.sleep(2)
            self.start()
            
    def home(self):
        print("""
                What would you like to do?
                1. Vote
                2. Check Vote result (general)
            """)
        do = input(">>>>> ")
        if do == "1":
            self.votestatus()
        elif do == "2":
            self.generalVote()

    def register(self):
        genalp = []
        gen = random.randint(111111111111,555555555555)
        gen = str(gen)
        query = "insert into students(fname, lname, voteID, password, gender, department, voted) values(%s, %s, %s, %s, %s, %s, %s)"
        for i in range(4):
            randomLetter = random.choice(string.ascii_uppercase)
            genalp.append(randomLetter)
        alp = ''.join(genalp)
        voteID = gen + alp
        fname = input("What is your first name: ")
        lname = input("what is your last name: ")
        password = input("Set a strong password: ")
        gen = input("What is your gender? Male or Female: ")
        dept = input("""Which department would you like to join
                        Choose one of the following
                        Dsc, Cyb, Web, Csc, Cse ?: """)
        info = ((fname, lname, voteID, password, gen, dept, "False"))
        mycursor.execute(query, info) 
        mydb.commit()
        print(f"Registration Successful, your name is {fname} {lname} and your unique Voting ID is {voteID}")
        time.sleep(1)
        self.login()
        
    def login(self):
        self.id = input("What is your Voting ID?: ")
        self.call = "select * from students where voteID = %s"
        self.val = (self.id, )
        mycursor.execute(self.call, self.val)
        self.user = mycursor.fetchone()
        # print(self.user)
        if self.user is None:
            print("Invalid Voting ID, try again")
            self.login()
        self.passw = input("Enter your password: ")
        if self.passw in self.user[4]:
            print("Login Successful")
            self.home()
        else:
            print("Incorrect Password, please try again")
            time.sleep(1)
            self.login()
      
    def votestatus(self):
        if self.user[7] == "True":
            print("You can only vote once!.") 
            time.sleep(2)
            self.home()
        elif self.user[7] == "False":
            self.vote()
        
    def vote(self):
        print("""
                            INSTRUCTIONS
            You can only vote once.
            You vote for your candidate by entering 'a' or 'b'.
            Any other input would be counted as INVALID i.e void.
            """)
        time.sleep(3)
        choice = []
        for i in self.candidate:
            index = self.candidate.index(i)
            print(self.candidate[index])
            print(self.options[index])
            user_vote = input("Choose your candidate: ")
            choice.append(user_vote)
        # print(choice)
        vtid = self.user[3]
        deprt = self.user[6]
        if choice[0] == "a":
            p = "Peter Gregory Obi"
        elif choice[0] == "b":
            p = "Ahmed Bola Tinubu"
        else:
            p = "Invalid"    
        if choice[1] == "a":
            vp = "Atiku Abubakar"
        elif choice[1] == "b":
            vp = "Yemi Osinbajo"
        else:
            vp = "Invalid"
        upv = "insert into votes (voterID, department, president, vicepresident) values (%s, %s, %s, %s)"
        mycursor.execute(upv, (vtid, deprt, p, vp))
        updv = "update students set voted = 'True' where voteID = %s"
        mycursor.execute(updv, (self.id, ))
        mydb.commit()
        time.sleep(2)
        print("You have successfully casted your vote")
                
    def generalVote(self):
        mycursor.execute("select president, vicepresident from votes")
        self.allvotes = mycursor.fetchall()
        obi = 0; bat = 0; atiku = 0; yemi = 0
        for i in self.allvotes:
            index = self.allvotes.index(i)
            if self.allvotes[index][0] == "Peter Gregory Obi":
                obi += 1   
            elif self.allvotes[index][0] == "Ahmed Bola Tinubu":
                bat += 1
            if self.allvotes[index][1] == "Atiku Abubakar":
                atiku += 1   
            elif self.allvotes[index][1] == "Yemi Osinbajo":
                yemi += 1
        if obi > bat:
            print("The winner of the Presidential Election is Peter Gregory Obi")
        elif bat > obi: 
            print("The winner of the Presidential Election is Ahmed Bola Tinubu")
        elif bat == obi:
            print("There is no winner for the Presidential Election, it is a TIE")
        if atiku > yemi:
            print("The winner of the Vice Presidential Election is Atiku Abubakar")
        elif yemi > atiku:
            print("The winner of the Vice Presidential Election is Yemi Osinbajo")
        elif yemi == atiku:
            print("There is no winner for the Vice Presidential Election, it is a TIE")
            
    # def deptVote(self):
    #     mycursor.execute("select department, president, vicepresident from votes")
    #     depts = mycursor.fetchall()
    #     for i in depts:
    #         index = depts.index(i)
            
        # print(depts
        # user should be able to check their vote option after voting
        
    
INEC() 