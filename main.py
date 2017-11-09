#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#imports
from google.appengine.ext import ndb
from google.appengine.api import users
import webapp2
import jinja2
import os
import json
import urllib
import urllib2
import datetime
import logging




jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

# user model for data store
class Score(ndb.Model):
    username = ndb.StringProperty()
    topic = ndb.StringProperty()
    score = ndb.IntegerProperty()
    time = ndb.DateTimeProperty()

class Submit(ndb.Model):
    question = ndb.StringProperty()
    answer = ndb.StringProperty()
    topicQ = ndb.StringProperty()

#main page handler
class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #sign in
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign In with Google</a>.' %
                users.create_login_url('/'))
        template_vars = {'greeting' : greeting }
        template = jinja_environment.get_template('templates/mainpage.html')
        self.response.write(template.render(template_vars))

# submit questions handlers
class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_environment.get_template('templates/submitQuestion.html')
        self.response.write(template.render())

    def post(self):
        question = self.request.get('question')
        answer = self.request.get('answer')
        topicQ = self.request.get('topicQ')
        logging.info(answer)
        new_Submit = Submit(question=question,answer= answer, topicQ=topicQ)
        new_Submit.put()
# creators page handler
class CreatorsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_environment.get_template('templates/creators.html')
        self.response.write(template.render())

# scores page handler
class ScoresHandler(webapp2.RequestHandler):
    def get (self):
        user = users.get_current_user()
        template = jinja_environment.get_template('templates/scoresPage.html')
        board= Score.query().order(-Score.time).fetch()
        logging.info(board)
        #marvel Score list
        # create list for marvel scores
        listMName=[]
        listMScore=[]
        tallyM=0
        # loop to add name and score at same indices
        for b in board:
            # if marvel then add it to the list
            if b.topic == "Marvel":
                listMName.append(b.username)
                listMScore.append(b.score)
                tallyM +=1
            # once 10 names have been stored break the loop
            if tallyM ==10:
                break
        #GOT score List
        listGName=[]
        listGScore=[]
        tallyG=0
        # loop to add name and score at same indices
        for b in board:
            # if marvel then add it to the list
            if b.topic == "GOT":
                listGName.append(b.username)
                listGScore.append(b.score)
                tallyG +=1
            # once 10 names have been stored break the loop
            if tallyG ==10:
                break
        #HArry Potter score list
        listHName=[]
        listHScore=[]
        tallyH=0
        # loop to add name and score at same indices
        #only get ten added to the list
        for b in board :
            # if marvel then add it to the list
            if b.topic == "Harry":
                listHName.append(b.username)
                listHScore.append(b.score)
                tallyH +=1
            # once 10 names have been stored break the loop
            if tallyH ==10:
                break
        logging.info(listGName)
        logging.info(listGScore)
        logging.info(listHName)
        logging.info(listHScore)

        #Avatar score list
        listAName=[]
        listAScore=[]
        tallyA=0
        # loop to add name and score at same indices
        #only get ten added to the list
        for b in board :
            # if marvel then add it to the list
            if b.topic == "Avatar":
                listAName.append(b.username)
                listAScore.append(b.score)
                tallyA +=1
            # once 10 names have been stored break the loop
            if tallyA ==10:
                break
        template_vars = {
         "boardMarvelnames": listMName,
         "boardMarvelscores":listMScore,
         "boardGOTnames": listGName,
         "boardGOTscores":listGScore,
         "boardHnames": listHName,
         "boardHscores":listHScore,
         "boardAnames": listAName,
         "boardAscores":listAScore
        }
        self.response.write(template.render(template_vars))


#marvel handler
class MarvelHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/quizMarvel.html')
        self.response.write(template.render())

    #check function to compatre to strings
    def check(self,answer, useranswer):
        if useranswer == answer:
            return True
        else:
            return False

    def post (self):
        user = users.get_current_user()
        totalScore = 0
        template = jinja_environment.get_template('templates/quizMarvelResults.html')
        #questions
        question1 = self.request.get('q1A')
        if self.check("chameleon",question1) == True:
            totalScore += 1
        logging.info(totalScore)
        #question2
        question2 = self.request.get('q2A')
        if self.check("parents",question2) == True:
            totalScore += 1
        #question3
        question3 = self.request.get('q3A')
        if self.check("luke",question3) == True:
            totalScore += 1
        #question4
        question4 = self.request.get('q4A')
        if self.check("real",question4) == True:
            totalScore += 1
        #question 5
        question5 = self.request.get('q5A')
        if self.check("clone",question5) == True:
            totalScore += 1
        #question6
        question6 = self.request.get('q6A')
        if self.check("wasp",question6) == True:
            totalScore += 1
        #question7
        question7 = self.request.get('q7A')
        if self.check("Hammer",question7) == True:
            totalScore += 1
        #questiion 8
        question8 = self.request.get('q8A')
        if self.check("spider",question8) == True:
            totalScore += 1
        #question 9
        question9 = self.request.get('q9A')
        if self.check("avengers",question9) == True:
            totalScore += 1
        #question 10
        question10 = self.request.get('q10A')
        if self.check("dead",question10) == True:
            totalScore += 1
        name=""
        # saving the user score based on their user google account
        if user:
            name= user.nickname()
        else:
            name = "Anonymous"
        #store data
        updateScore= Score(username= name, topic = "Marvel", score = totalScore, time=datetime.datetime.now() )
        updateScore.put()
        #fetching data
        board= Score.query().order(-Score.time).fetch(limit=10)
        logging.info(board)
        # create loop
        listName=[]
        listScore=[]
        tally= 0
        # loop to add name and score at same indices
        for b in board:
            # if marvel then add it to the list
            if b.topic == "Marvel":
                listName.append(b.username)
                listScore.append(b.score)
                tally += 1
            if tally == 10:
                break
        template_vars = {
         "score" : totalScore,
         "boardnames": listName,
         "boardscores":listScore
        }
        self.response.write(template.render(template_vars))
#game of thrones
class GOTHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/quizGOT.html')
        self.response.write(template.render())

    def check(self, answer, useranswer):
        logging.info(useranswer)
        logging.info(answer)
        if useranswer == answer:
            return True
        else:
            return False

    def post (self):
        user = users.get_current_user()
        totalScore = 0
        template = jinja_environment.get_template('templates/quizGOTResults.html')
        #questions
        question1 = self.request.get('q1A')
        if self.check("answer",question1) == True:
            totalScore += 1
        logging.info(totalScore)
        #question2
        question2 = self.request.get('q2A')
        if self.check("answer",question2) == True:
            totalScore += 1
        #question3
        question3 = self.request.get('q3A')
        if self.check("answer",question3) == True:
            totalScore += 1
        #question4
        question4 = self.request.get('q4A')
        if self.check("answer",question4) == True:
            totalScore += 1
        #question 5
        question5 = self.request.get('q5A')
        if self.check("answer",question5) == True:
            totalScore += 1
        #question6
        question6 = self.request.get('q6A')
        if self.check("answer",question6) == True:
            totalScore += 1
        #question7
        question7 = self.request.get('q7A')
        if self.check("answer",question7) == True:
            totalScore += 1
        #questiion 8
        question8 = self.request.get('q8A')
        if self.check("answer",question8) == True:
            totalScore += 1
        #question 9
        question9 = self.request.get('q9A')
        if self.check("answer",question9) == True:
            totalScore += 1
        #question 10
        question10 = self.request.get('q10A')
        if self.check("answer",question10) == True:
            totalScore += 1
        name=""
        # saving the user score based on their user google account
        if user:
            name= user.nickname()
        else:
            name = "Anonymous"
        #store data
        updateScore= Score(username= name, topic = "GOT", score = totalScore, time=datetime.datetime.now() )
        updateScore.put()
        #fetching data
        board= Score.query().order(-Score.time).fetch(limit=10)
        logging.info(board)
        # create loop
        listName=[]
        listScore=[]
        tally =0
        # loop to add name and score at same indices
        for b in board:
            if b.topic == "GOT":
                listName.append(b.username)
                listScore.append(b.score)
                tally += 1
            if tally == 10:
                break
        template_vars = {
         "score" : totalScore,
         "boardnames": listName,
         "boardscores":listScore
        }
        self.response.write(template.render(template_vars))


class SportsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/quizSports.html')
        self.response.write(template.render())

    def check(self, answer, useranswer):
        logging.info(useranswer)
        logging.info(answer)
        if useranswer == answer:
            return True
        else:
            return False

    def post (self):
        user = users.get_current_user()
        totalScore = 0
        template = jinja_environment.get_template('templates/quizSportsResults.html')
        #questions
        question1 = self.request.get('q1A')
        if self.check("answer",question1) == True:
            totalScore += 1
        logging.info(totalScore)
        #question2
        question2 = self.request.get('q2A')
        if self.check("answer",question2) == True:
            totalScore += 1
        #question3
        question3 = self.request.get('q3A')
        if self.check("answer",question3) == True:
            totalScore += 1
        #question4
        question4 = self.request.get('q4A')
        if self.check("answer",question4) == True:
            totalScore += 1
        #question 5
        question5 = self.request.get('q5A')
        if self.check("answer",question5) == True:
            totalScore += 1
        #question6
        question6 = self.request.get('q6A')
        if self.check("answer",question6) == True:
            totalScore += 1
        #question7
        question7 = self.request.get('q7A')
        if self.check("answer",question7) == True:
            totalScore += 1
        #questiion 8
        question8 = self.request.get('q8A')
        if self.check("answer",question8) == True:
            totalScore += 1
        #question 9
        question9 = self.request.get('q9A')
        if self.check("answer",question9) == True:
            totalScore += 1
        #question 10
        question10 = self.request.get('q10A')
        if self.check("answer",question10) == True:
            totalScore += 1

        name=""
        # saving the user score based on their user google account
        if user:
            name= user.nickname()
        else:
            name = "Anonymous"
        #store data
        updateScore= Score(username= name, topic = "Harry", score = totalScore, time=datetime.datetime.now() )
        updateScore.put()
        #fetching data
        board= Score.query().order(-Score.time).fetch(limit=10)
        logging.info(board)
        # create loop
        listName=[]
        listScore=[]
        tally =0
        # loop to add name and score at same indices
        for b in board:
            if b.topic == "Harry":
                listName.append(b.username)
                listScore.append(b.score)
                tally += 1
            if tally == 10:
                break
        template_vars = {
         "score" : totalScore,
         "boardnames": listName,
         "boardscores":listScore
        }
        self.response.write(template.render(template_vars))

#avatar handler
class AvatarHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/quizAvatar.html')
        self.response.write(template.render())

    def check(self, answer, useranswer):
        logging.info(useranswer)
        logging.info(answer)
        if useranswer == answer:
            return True
        else:
            return False

    def post (self):
        user = users.get_current_user()
        totalScore = 0
        template = jinja_environment.get_template('templates/quizAvatarResults.html')
        #questions
        question1 = self.request.get('q1A')
        if self.check("answer",question1) == True:
            totalScore += 1
        logging.info(totalScore)
        #question2
        question2 = self.request.get('q2A')
        if self.check("answer",question2) == True:
            totalScore += 1
        #question3
        question3 = self.request.get('q3A')
        if self.check("answer",question3) == True:
            totalScore += 1
        #question4
        question4 = self.request.get('q4A')
        if self.check("answer",question4) == True:
            totalScore += 1
        #question 5
        question5 = self.request.get('q5A')
        if self.check("answer",question5) == True:
            totalScore += 1
        #question6
        question6 = self.request.get('q6A')
        if self.check("answer",question6) == True:
            totalScore += 1
        #question7
        question7 = self.request.get('q7A')
        if self.check("answer",question7) == True:
            totalScore += 1
        #questiion 8
        question8 = self.request.get('q8A')
        if self.check("answer",question8) == True:
            totalScore += 1
        #question 9
        question9 = self.request.get('q9A')
        if self.check("answer",question9) == True:
            totalScore += 1
        #question 10
        question10 = self.request.get('q10A')
        if self.check("answer",question10) == True:
            totalScore += 1

        name=""
        # saving the user score based on their user google account
        if user:
            name= user.nickname()
        else:
            name = "Anonymous"
        #store data
        updateScore= Score(username= name, topic = "Avatar", score = totalScore, time=datetime.datetime.now() )
        updateScore.put()
        #fetching data
        board= Score.query().order(-Score.time).fetch(limit=10)
        logging.info(board)
        # create loop
        listName=[]
        listScore=[]
        tally =0
        # loop to add name and score at same indices
        for b in board:
            if b.topic == "Avatar":
                listName.append(b.username)
                listScore.append(b.score)
                tally += 1
            if tally == 10:
                break
        template_vars = {
         "score" : totalScore,
         "boardnames": listName,
         "boardscores":listScore
        }
        self.response.write(template.render(template_vars))


#answer handler
class AnswerHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_environment.get_template('templates/answers.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit',SubmitHandler),
    ('/us',CreatorsHandler),
    ('/scores',ScoresHandler),
    ('/marvel', MarvelHandler),
    ('/got', GOTHandler),
    ('/sports', SportsHandler),
    ('/avatar',AvatarHandler),
    ('/answers', AnswerHandler)
], debug=True)
