# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'liveMatch.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from changeBowler import Ui_changeBowler
from PyQt5 import QtCore, QtGui, QtWidgets

class Batsman():
    def __init__(self, name):
        self.name=name
        self.runs=0
        self.balls=0
        self.fours=0
        self.sixes=0
    def addRuns(self,run):
        self.runs+=run
        if run==4 or run==5:
            self.fours+=1
        elif run==6:
            self.sixes+=1
    def incrementBall(self):
        self.balls+=1

class Bowler():
    def __init__(self, name):
        self.name=name
        self.runs=0
        self.overs=0
        self.balls=0
        self.maidens=0
        self.wickets=0
        self.thisOver=0
    def addRuns(self,run):
        self.runs+=run
        self.thisOver+=run
    def updateOver(self):
        self.balls+=1
        if self.balls==6:
            self.overs += 1
            self.balls = 0
            if self.thisOver==0:
                self.maidens+=1
            self.thisOver=0
    def updateWicket(self):
        self.wickets+=1

class Team():
    def __init__(self, team):
        self.name=team[0]
        self.wicketKeeper=team[1]
        self.captain=team[2]
        self.players=team[2:]
        self.score=0
        self.wickets=0
        self.extras=0
        self.overs=0
        self.balls=0
    def updateScore(self , runs, extra=0):
        self.score += runs + extra
        self.extras += extra
    def updateWicket(self):
        self.wickets+=1
    def updateOver(self):
        self.balls+=1
        if self.balls==6:
            self.overs += 1
            self.balls = 0
            return True
        return False
        

class Ui_matchPage(object):

    def updateBatsman(self):
        self.strikerName.setText(f'{self.striker.name}*')
        self.strikerRunBall.setText(f'{self.striker.runs}({self.striker.balls})')
        self.nonStrikerName.setText(f'{self.nonStriker.name}')
        self.nonStrikerRunBall.setText(f'{self.nonStriker.runs}({self.nonStriker.balls})')

    def updateBowler(self):
        self.bowlerName.setText(f'{self.currBowler.name}')
        self.bowlerStats.setText(f'{self.currBowler.runs}/{self.currBowler.wickets}  ({self.currBowler.overs}.{self.currBowler.balls})')

    def updateTeamsScore(self, team1, team2):
        if self.inning1==True:
            self.updateTeam1(team1)
        else:
            self.updateTeam2(team2)

    def updateTeam1(self,team):
        self.team1Score.setText(f'{team.score}/{team.wickets}')
        self.team1Over.setText(f"{team.overs}.{team.balls}")

    def updateTeam2(self,team):
        self.team2Score.setText(f'{team.score}/{team.wickets}')
        self.team2Over.setText(f"{team.overs}.{team.balls}")

    def updateAvailableBowler(self):
        if self.prevBowler!=None:
            self.availableBowlers.insert(0,self.prevBowler)
        if self.currBowler.overs<self.oversLimit:
            self.prevBowler=self.currBowler.name
        else:
            self.prevBowler=None

    def onClickButton(self, val):
        #written by Tafzeel
        thisBall=f'{val}'
        extra=0
        run=0
        legalBall=False
        endOver=False
        wicketFall=False
        if self.isLegBye.isChecked() and self.isWide.isChecked():
            print("Not possible")
            return
        if self.isLegBye.isChecked() and self.isBye.isChecked():
            print("Not possible")
            return
        if self.isWide.isChecked() and self.isNoBall.isChecked():
            print("Not possible")
            return
        if self.isWide.isChecked():
            extra = val+1
            thisBall=f'{val}WD'
            self.currBowler.addRuns(extra)
        elif self.isNoBall.isChecked():
            if self.isLegBye.isChecked():
                extra=val+1
                thisBall=f'{val}(LB)NB'
            elif self.isBye.isChecked():
                extra=val+1
                thisBall=f'{val}(B)NB'
            else:
                run=val
                extra=1
                thisBall=f'{val}NB'
                self.striker.addRuns(run)
            self.currBowler.addRuns(run+extra)
        else:
            legalBall=True
            if self.isLegBye.isChecked():
                thisBall=f'{val}LB'
                extra=val
            elif self.isBye.isChecked():
                thisBall=f'{val}B'
                extra=val
            else:
                run=val
                thisBall=f'{val}'
                self.striker.addRuns(run)
            self.striker.incrementBall()
            self.currBowler.addRuns(run)
            self.currBowler.updateOver()
        if val%2==1:
            self.onClickSwapBatsman()
        if self.isWicket.isChecked():
            print("OUT")
            thisBall='W'
            wicketFall=True#new Window
            self.currBowler.updateWicket()
            self.striker=Batsman(self.availableBatsman.pop(0))
            #check for wicket type
            if self.inning1:
                self.battingInnings1.append(self.striker.name)
            else:
                self.battingInnings2.append(self.striker.name)
            #update DataBase
        self.thisOverString =self.thisOverString + '  ' + thisBall
        self.thisOver.setText(self.thisOverString)
        if self.inning1 == True:
            self.team1.updateScore(run,extra)
            if wicketFall:
                self.team1.updateWicket()
            if legalBall:
                endOver = self.team1.updateOver()
        else:
            self.team2.updateScore(run,extra)
            if wicketFall:
                self.team2.updateWicket()
            if legalBall:
                endOver = self.team2.updateOver()
        if endOver:
            self.updateAvailableBowler()
            self.onClickSwapBatsman()
            self.thisOverString=''
            if (self.inning1 and self.team1.overs!=self.maxOvers) or (self.inning1==False and self.team2.overs!=self.maxOvers):
                #open new Window
                #self.newBowler = self.openChangeBowler(self.availableBowlers[:])
                self.newBowler =self.availableBowlers[0]
                print(self.newBowler)
                if self.newBowler in self.bowlersBowled:
                    if self.inning1:
                        for bowler in self.bowlingInning1:
                            if self.newBowler==bowler.name:
                                self.currBowler=bowler
                                break
                    else:
                        for bowler in self.bowlingInning2:
                            if self.newBowler==bowler.name:
                                self.currBowler=bowler
                                break                    
                else:
                    self.bowlersBowled.add(self.newBowler)
                    self.currBowler=Bowler(self.newBowler)
                    if self.inning1:
                        self.bowlingInning1.append(self.currBowler)
                self.availableBowlers.remove(self.currBowler.name)
        self.updateTeamsScore(self.team1,self.team2)
        self.updateBatsman()
        self.updateBowler()
        self.isWicket.setChecked(False)
        self.isBye.setChecked(False)
        self.isWide.setChecked(False)
        self.isNoBall.setChecked(False)
        self.isLegBye.setChecked(False)
        self.checkEndOfInnings()

    #def openChangeBowler(self, bowlerList):
        #select Bowler
    
    def onClick6(self):
        self.onClickButton(6)

    def onClick5(self):
        self.onClickButton(5)

    def onClick4(self):
        self.onClickButton(4)

    def onClick3(self):
        self.onClickButton(3)

    def onClick2(self):
        self.onClickButton(2)  

    def onClick1(self):
        self.onClickButton(1)

    def onClick0(self):
        self.onClickButton(0)

    def onClickSwapBatsman(self):
        ##written by Tafzeel
        self.striker, self.nonStriker = self.nonStriker, self.striker
        self.updateBatsman()

    def checkEndOfInnings(self):
        if  self.inning1:
            if self.team1.overs==self.maxOvers or self.team1.wickets==10:
                self.changeInnings()
                #end Innings
        else:
            if self.team2.overs==self.maxOvers or self.team2.wickets==10 or self.team2.score>=self.target:
                self.endMatch()
                #end Match

    def changeInnings(self):
        ##Added by Tafzeel
        self.target=self.team1.score+1
        self.inning1=False
        self.thisOverString=''
        self.availableBowlers=self.team1.players[:]
        self.availableBowlers.remove(self.team1.wicketKeeper)
        self.availableBatsman=self.team2.players[:]
        self.bowlersBowled=set()
        self.currBowler=Bowler('Dale Steyn')
        self.striker=Batsman("Shane Watson")
        self.nonStriker=Batsman("Faf Du Plesis")
        self.bowlersBowled.add("Dale Steyn")
        self.availableBowlers.remove(self.currBowler.name)
        self.availableBatsman.remove(self.striker.name)
        self.availableBatsman.remove(self.nonStriker.name)
        self.battingInnings2=[self.striker,self.nonStriker]
        self.bowlingInning2=[self.currBowler]
        self.updateBatsman()
        self.updateBowler()
        self.updateTeamsScore(self.team1,self.team2)
        self.thisOver.setText(self.thisOverString)
        self.matchStatus.setText(f'Target : {self.target}')

    def endMatch(self):
        #Added by Tafzeel
        if self.team2.score>=self.target:
            print(f'{self.team2.name} WON')
        else:
            print(f'{self.team1.name} WON')

    def setupUi(self, matchPage, toss, team1, team2):
        ##Added By Tafzeel
        tossStatus=f'{toss[0]} elected  to {toss[1]}'
        if toss[0]==team1[0]:
            if toss[1]=='Feild First':
                team1, team2 = team2, team1
        else:
            if toss[1]=='Bat First':
                team1, team2 = team2, team1
        self.inning1=True
        self.maxOvers=toss[2]
        self.oversLimit=self.maxOvers//5
        if self.maxOvers%5 != 0:
            self.oversLimit += 1
        self.team1 = Team(team1)
        self.team2 =Team(team2)
        ######print(team1[0])
        self.thisOverString=''
        self.availableBowlers=self.team2.players[:]
        self.availableBowlers.remove(self.team2.wicketKeeper)
        self.availableBatsman=self.team1.players[:]
        #call for newInning
        #######print(self.team1)
        self.newBowler='Imran Tahir'
        self.currBowler=Bowler(self.newBowler)
        self.striker=Batsman("Parthiv Patel")
        self.nonStriker=Batsman("Virat Kohli")
        ########print(self.availableBowlers)
        self.bowlersBowled=set()
        self.bowlersBowled.add(self.newBowler)
        self.availableBowlers.remove(self.currBowler.name)
        self.availableBatsman.remove(self.striker.name)
        self.availableBatsman.remove(self.nonStriker.name)
        self.battingInnings1=[self.striker,self.nonStriker]
        self.bowlingInning1=[self.currBowler]
        self.battingInnings2=[]
        self.bowlingInning2=[]
        self.prevBowler=None
        ###
        matchPage.setObjectName("matchPage")
        matchPage.setEnabled(True)
        matchPage.resize(1724, 895)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(matchPage.sizePolicy().hasHeightForWidth())
        matchPage.setSizePolicy(sizePolicy)
        matchPage.setMinimumSize(QtCore.QSize(0, 0))
        matchPage.setMaximumSize(QtCore.QSize(10000, 6000))
        matchPage.setWindowOpacity(1.0)
        matchPage.setStyleSheet("background-color: rgb(11, 12, 16);")
        self.matchFrame = QtWidgets.QFrame(matchPage)
        self.matchFrame.setEnabled(True)
        self.matchFrame.setGeometry(QtCore.QRect(10, 10, 1701, 881))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matchFrame.sizePolicy().hasHeightForWidth())
        self.matchFrame.setSizePolicy(sizePolicy)
        self.matchFrame.setObjectName("matchFrame")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.matchFrame)
        self.gridLayout_7.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.matchSummaryWidget = QtWidgets.QWidget(self.matchFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matchSummaryWidget.sizePolicy().hasHeightForWidth())
        self.matchSummaryWidget.setSizePolicy(sizePolicy)
        self.matchSummaryWidget.setObjectName("matchSummaryWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.matchSummaryWidget)
        self.gridLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.matchStatus = QtWidgets.QLabel(self.matchSummaryWidget)
        self.matchStatus.setMaximumSize(QtCore.QSize(16777215, 38))
        self.matchStatus.setStyleSheet("background-color: rgb(69, 162, 158);")
        self.matchStatus.setObjectName("matchStatus")
        self.gridLayout_6.addWidget(self.matchStatus, 0, 0, 1, 1)
        self.teamsScore = QtWidgets.QWidget(self.matchSummaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teamsScore.sizePolicy().hasHeightForWidth())
        self.teamsScore.setSizePolicy(sizePolicy)
        self.teamsScore.setStyleSheet("background-color: rgb(31, 40, 51);")
        self.teamsScore.setObjectName("teamsScore")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.teamsScore)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.inning1Score = QtWidgets.QWidget(self.teamsScore)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inning1Score.sizePolicy().hasHeightForWidth())
        self.inning1Score.setSizePolicy(sizePolicy)
        self.inning1Score.setStyleSheet("background-color: rgb(31, 40, 51); color: rgb(197, 198, 199);")
        self.inning1Score.setObjectName("inning1Score")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.inning1Score)
        self.verticalLayout.setObjectName("verticalLayout")
        self.team1Name = QtWidgets.QLabel(self.inning1Score)
        self.team1Name.setStyleSheet("font: 24pt \"Cantarell\";")
        self.team1Name.setScaledContents(False)
        self.team1Name.setObjectName("team1Name")
        self.verticalLayout.addWidget(self.team1Name, 0, QtCore.Qt.AlignHCenter)
        self.team1Score = QtWidgets.QLabel(self.inning1Score)
        self.team1Score.setStyleSheet("font: 20pt \"Cantarell\";")
        self.team1Score.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.team1Score.setObjectName("team1Score")
        self.verticalLayout.addWidget(self.team1Score, 0, QtCore.Qt.AlignHCenter)
        self.team1OversWidget = QtWidgets.QWidget(self.inning1Score)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.team1OversWidget.sizePolicy().hasHeightForWidth())
        self.team1OversWidget.setSizePolicy(sizePolicy)
        self.team1OversWidget.setObjectName("team1OversWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.team1OversWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.oversLabel1 = QtWidgets.QLabel(self.team1OversWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.oversLabel1.sizePolicy().hasHeightForWidth())
        self.oversLabel1.setSizePolicy(sizePolicy)
        self.oversLabel1.setStyleSheet("font: 16pt \"Cantarell\";")
        self.oversLabel1.setObjectName("oversLabel1")
        self.horizontalLayout.addWidget(self.oversLabel1, 0, QtCore.Qt.AlignRight)
        self.team1Over = QtWidgets.QLabel(self.team1OversWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.team1Over.sizePolicy().hasHeightForWidth())
        self.team1Over.setSizePolicy(sizePolicy)
        self.team1Over.setStyleSheet("font: 17pt \"Cantarell\";")
        self.team1Over.setObjectName("team1Over")
        self.horizontalLayout.addWidget(self.team1Over, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.team1OversWidget)
        self.gridLayout_3.addWidget(self.inning1Score, 0, 0, 1, 1)
        self.inning2Score = QtWidgets.QWidget(self.teamsScore)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inning2Score.sizePolicy().hasHeightForWidth())
        self.inning2Score.setSizePolicy(sizePolicy)
        self.inning2Score.setStyleSheet("background-color: rgb(31, 40, 51); color: rgb(197, 198, 199);")
        self.inning2Score.setObjectName("inning2Score")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.inning2Score)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.team2Name = QtWidgets.QLabel(self.inning2Score)
        self.team2Name.setStyleSheet("font: 24pt \"Cantarell\";")
        self.team2Name.setObjectName("team2Name")
        self.verticalLayout_2.addWidget(self.team2Name, 0, QtCore.Qt.AlignHCenter)
        self.team2Score = QtWidgets.QLabel(self.inning2Score)
        self.team2Score.setStyleSheet("font: 20pt \"Cantarell\";")
        self.team2Score.setObjectName("team2Score")
        self.verticalLayout_2.addWidget(self.team2Score, 0, QtCore.Qt.AlignHCenter)
        self.team2OversWidget = QtWidgets.QWidget(self.inning2Score)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.team2OversWidget.sizePolicy().hasHeightForWidth())
        self.team2OversWidget.setSizePolicy(sizePolicy)
        self.team2OversWidget.setObjectName("team2OversWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.team2OversWidget)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.oversLabel2 = QtWidgets.QLabel(self.team2OversWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.oversLabel2.sizePolicy().hasHeightForWidth())
        self.oversLabel2.setSizePolicy(sizePolicy)
        self.oversLabel2.setStyleSheet("font: 16pt \"Cantarell\";")
        self.oversLabel2.setObjectName("oversLabel2")
        self.horizontalLayout_2.addWidget(self.oversLabel2, 0, QtCore.Qt.AlignRight)
        self.team2Over = QtWidgets.QLabel(self.team2OversWidget)
        self.team2Over.setStyleSheet("font: 17pt \"Cantarell\";")
        self.team2Over.setObjectName("team2Over")
        self.horizontalLayout_2.addWidget(self.team2Over)
        self.verticalLayout_2.addWidget(self.team2OversWidget)
        self.gridLayout_3.addWidget(self.inning2Score, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.teamsScore)
        self.line.setStyleSheet("color: rgb(69, 162, 158); background-color: rgb(69, 162, 158);")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.teamsScore, 1, 0, 1, 1)
        self.batsmanWidget = QtWidgets.QWidget(self.matchSummaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.batsmanWidget.sizePolicy().hasHeightForWidth())
        self.batsmanWidget.setSizePolicy(sizePolicy)
        self.batsmanWidget.setObjectName("batsmanWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.batsmanWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.strikerWidget = QtWidgets.QWidget(self.batsmanWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.strikerWidget.sizePolicy().hasHeightForWidth())
        self.strikerWidget.setSizePolicy(sizePolicy)
        self.strikerWidget.setStyleSheet("background-color: rgb(69, 162, 158); color: rgb(31, 40, 51);")
        self.strikerWidget.setObjectName("strikerWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.strikerWidget)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.strikerName = QtWidgets.QLabel(self.strikerWidget)
        self.strikerName.setStyleSheet("font: 18pt \"Cantarell\";")
        self.strikerName.setObjectName("strikerName")
        self.horizontalLayout_3.addWidget(self.strikerName)
        self.strikerRunBall = QtWidgets.QLabel(self.strikerWidget)
        self.strikerRunBall.setStyleSheet("font: 18pt \"Cantarell\";")
        self.strikerRunBall.setObjectName("strikerRunBall")
        self.horizontalLayout_3.addWidget(self.strikerRunBall, 0, QtCore.Qt.AlignRight)
        self.gridLayout_4.addWidget(self.strikerWidget, 0, 0, 1, 1)
        self.nonStrikerWidget = QtWidgets.QWidget(self.batsmanWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nonStrikerWidget.sizePolicy().hasHeightForWidth())
        self.nonStrikerWidget.setSizePolicy(sizePolicy)
        self.nonStrikerWidget.setStyleSheet("background-color: rgb(69, 162, 158); color: rgb(31, 40, 51);")
        self.nonStrikerWidget.setObjectName("nonStrikerWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.nonStrikerWidget)
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.nonStrikerName = QtWidgets.QLabel(self.nonStrikerWidget)
        self.nonStrikerName.setStyleSheet("font: 18pt \"Cantarell\";")
        self.nonStrikerName.setObjectName("nonStrikerName")
        self.horizontalLayout_4.addWidget(self.nonStrikerName)
        self.nonStrikerRunBall = QtWidgets.QLabel(self.nonStrikerWidget)
        self.nonStrikerRunBall.setStyleSheet("font: 18pt \"Cantarell\";")
        self.nonStrikerRunBall.setObjectName("nonStrikerRunBall")
        self.horizontalLayout_4.addWidget(self.nonStrikerRunBall, 0, QtCore.Qt.AlignRight)
        self.gridLayout_4.addWidget(self.nonStrikerWidget, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.batsmanWidget, 3, 0, 1, 1)
        self.oversWidget = QtWidgets.QWidget(self.matchSummaryWidget)
        self.oversWidget.setObjectName("oversWidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.oversWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.thisOverWidget = QtWidgets.QWidget(self.oversWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thisOverWidget.sizePolicy().hasHeightForWidth())
        self.thisOverWidget.setSizePolicy(sizePolicy)
        self.thisOverWidget.setStyleSheet("background-color: rgb(69, 162, 158); color: rgb(31, 40, 51);")
        self.thisOverWidget.setObjectName("thisOverWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.thisOverWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.thisOver = QtWidgets.QLabel(self.thisOverWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thisOver.sizePolicy().hasHeightForWidth())
        self.thisOver.setSizePolicy(sizePolicy)
        self.thisOver.setStyleSheet("font: 18pt \"Cantarell\";")
        self.thisOver.setObjectName("thisOver")
        self.verticalLayout_4.addWidget(self.thisOver, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_5.addWidget(self.thisOverWidget, 0, 1, 1, 1)
        self.bowlwerWidget = QtWidgets.QWidget(self.oversWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bowlwerWidget.sizePolicy().hasHeightForWidth())
        self.bowlwerWidget.setSizePolicy(sizePolicy)
        self.bowlwerWidget.setStyleSheet("background-color: rgb(69, 162, 158); color: rgb(31, 40, 51);")
        self.bowlwerWidget.setObjectName("bowlwerWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.bowlwerWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bowlerName = QtWidgets.QLabel(self.bowlwerWidget)
        self.bowlerName.setStyleSheet("font: 18pt \"Cantarell\";")
        self.bowlerName.setObjectName("bowlerName")
        self.verticalLayout_3.addWidget(self.bowlerName, 0, QtCore.Qt.AlignHCenter)
        self.bowlerStats = QtWidgets.QLabel(self.bowlwerWidget)
        self.bowlerStats.setStyleSheet("font: 16pt \"Cantarell\";")
        self.bowlerStats.setObjectName("bowlerStats")
        self.verticalLayout_3.addWidget(self.bowlerStats, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_5.addWidget(self.bowlwerWidget, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.oversWidget, 4, 0, 1, 1)
        self.optionsWidget = QtWidgets.QWidget(self.matchSummaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionsWidget.sizePolicy().hasHeightForWidth())
        self.optionsWidget.setSizePolicy(sizePolicy)
        self.optionsWidget.setStyleSheet("background-color: rgb(17, 100, 102); background-color: rgb(44, 53, 49);")
        self.optionsWidget.setObjectName("optionsWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.optionsWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.isLegBye = QtWidgets.QCheckBox(self.optionsWidget)
        self.isLegBye.setStyleSheet("color: rgb(102, 252, 241);")
        self.isLegBye.setObjectName("isLegBye")
        self.gridLayout.addWidget(self.isLegBye, 1, 1, 1, 1)
        self.isBye = QtWidgets.QCheckBox(self.optionsWidget)
        self.isBye.setStyleSheet("color: rgb(102, 252, 241);")
        self.isBye.setObjectName("isBye")
        self.gridLayout.addWidget(self.isBye, 1, 0, 1, 1)
        self.isWide = QtWidgets.QCheckBox(self.optionsWidget)
        self.isWide.setStyleSheet("color: rgb(102, 252, 241);")
        self.isWide.setObjectName("isWide")
        self.gridLayout.addWidget(self.isWide, 0, 0, 1, 1)
        self.isWicket = QtWidgets.QCheckBox(self.optionsWidget)
        self.isWicket.setStyleSheet("color: rgb(102, 252, 241);")
        self.isWicket.setObjectName("isWicket")
        self.gridLayout.addWidget(self.isWicket, 0, 2, 1, 1)
        self.isNoBall = QtWidgets.QCheckBox(self.optionsWidget)
        self.isNoBall.setStyleSheet("color: rgb(102, 252, 241);")
        self.isNoBall.setObjectName("isNoBall")
        self.gridLayout.addWidget(self.isNoBall, 0, 1, 1, 1)
        self.swapBatsmanButton = QtWidgets.QPushButton(self.optionsWidget)
        self.swapBatsmanButton.setStyleSheet("background-color: rgb(102, 252, 241); color: rgb(31, 40, 51);")
        self.swapBatsmanButton.setObjectName("swapBatsmanButton")
        self.gridLayout.addWidget(self.swapBatsmanButton, 1, 2, 1, 1)
        self.applyDLButton = QtWidgets.QPushButton(self.optionsWidget)
        self.applyDLButton.setStyleSheet("background-color: rgb(102, 252, 241); color: rgb(31, 40, 51);")
        self.applyDLButton.setObjectName("applyDLButton")
        self.gridLayout.addWidget(self.applyDLButton, 0, 3, 1, 1)
        self.endMatchButton = QtWidgets.QPushButton(self.optionsWidget)
        self.endMatchButton.setStyleSheet("background-color: rgb(102, 252, 241); color: rgb(31, 40, 51);")
        self.endMatchButton.setObjectName("endMatchButton")
        self.gridLayout.addWidget(self.endMatchButton, 1, 3, 1, 1)
        self.gridLayout_6.addWidget(self.optionsWidget, 6, 0, 1, 1)
        self.scorerWidget = QtWidgets.QWidget(self.matchSummaryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scorerWidget.sizePolicy().hasHeightForWidth())
        self.scorerWidget.setSizePolicy(sizePolicy)
        self.scorerWidget.setStyleSheet("")
        self.scorerWidget.setObjectName("scorerWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scorerWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button3 = QtWidgets.QPushButton(self.scorerWidget)
        self.button3.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button3.setObjectName("button3")
        self.gridLayout_2.addWidget(self.button3, 0, 3, 1, 1)
        self.button6 = QtWidgets.QPushButton(self.scorerWidget)
        self.button6.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button6.setObjectName("button6")
        self.gridLayout_2.addWidget(self.button6, 2, 2, 1, 1)
        self.button5 = QtWidgets.QPushButton(self.scorerWidget)
        self.button5.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button5.setObjectName("button5")
        self.gridLayout_2.addWidget(self.button5, 2, 1, 1, 1)
        self.button2 = QtWidgets.QPushButton(self.scorerWidget)
        self.button2.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button2.setObjectName("button2")
        self.gridLayout_2.addWidget(self.button2, 0, 2, 1, 1)
        self.buttonEndInnings = QtWidgets.QPushButton(self.scorerWidget)
        self.buttonEndInnings.setStyleSheet("background-color: rgb(102, 252, 241);")
        self.buttonEndInnings.setObjectName("buttonEndInnings")
        self.gridLayout_2.addWidget(self.buttonEndInnings, 2, 3, 1, 1)
        self.button4 = QtWidgets.QPushButton(self.scorerWidget)
        self.button4.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button4.setObjectName("button4")
        self.gridLayout_2.addWidget(self.button4, 2, 0, 1, 1)
        self.button1 = QtWidgets.QPushButton(self.scorerWidget)
        self.button1.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button1.setObjectName("button1")
        self.gridLayout_2.addWidget(self.button1, 0, 1, 1, 1)
        self.button0 = QtWidgets.QPushButton(self.scorerWidget)
        self.button0.setStyleSheet("color: rgb(102, 252, 241); background-color: rgb(31, 40, 51);")
        self.button0.setObjectName("button0")
        self.gridLayout_2.addWidget(self.button0, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.scorerWidget, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_6.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 5, 0, 1, 1)
        self.gridLayout_7.addWidget(self.matchSummaryWidget, 0, 0, 1, 1)
        self.scoreCardWidget = QtWidgets.QWidget(self.matchFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scoreCardWidget.sizePolicy().hasHeightForWidth())
        self.scoreCardWidget.setSizePolicy(sizePolicy)
        self.scoreCardWidget.setObjectName("scoreCardWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scoreCardWidget)
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scoreCardTab = QtWidgets.QTabWidget(self.scoreCardWidget)
        self.scoreCardTab.setStyleSheet("background-color: rgb(31, 40, 51); color: rgb(102, 252, 241);")
        self.scoreCardTab.setObjectName("scoreCardTab")
        self.firstInningTab = QtWidgets.QWidget()
        self.firstInningTab.setObjectName("firstInningTab")
        self.tabWidget = QtWidgets.QTabWidget(self.firstInningTab)
        self.tabWidget.setGeometry(QtCore.QRect(6, 9, 631, 791))
        self.tabWidget.setStyleSheet("background-color: rgb(17, 100, 102); color: rgb(197, 198, 199);")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.batting1Tab = QtWidgets.QWidget()
        self.batting1Tab.setObjectName("batting1Tab")
        self.batting1TableWidget = QtWidgets.QTableWidget(self.batting1Tab)
        self.batting1TableWidget.setGeometry(QtCore.QRect(5, 11, 581, 761))
        self.batting1TableWidget.setObjectName("batting1TableWidget")
        self.batting1TableWidget.setColumnCount(0)
        self.batting1TableWidget.setRowCount(0)
        self.tabWidget.addTab(self.batting1Tab, "")
        self.bowling1Tab = QtWidgets.QWidget()
        self.bowling1Tab.setObjectName("bowling1Tab")
        self.bowling1TableWidget = QtWidgets.QTableWidget(self.bowling1Tab)
        self.bowling1TableWidget.setGeometry(QtCore.QRect(10, 10, 581, 771))
        self.bowling1TableWidget.setObjectName("bowling1TableWidget")
        self.bowling1TableWidget.setColumnCount(0)
        self.bowling1TableWidget.setRowCount(0)
        self.tabWidget.addTab(self.bowling1Tab, "")
        self.scoreCardTab.addTab(self.firstInningTab, "")
        self.scondInningTab = QtWidgets.QWidget()
        self.scondInningTab.setObjectName("scondInningTab")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.scondInningTab)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 10, 631, 791))
        self.tabWidget_2.setStyleSheet("background-color: rgb(17, 100, 102); color: rgb(197, 198, 199);")
        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.batting2Tab = QtWidgets.QWidget()
        self.batting2Tab.setObjectName("batting2Tab")
        self.batting2TableWidget = QtWidgets.QTableWidget(self.batting2Tab)
        self.batting2TableWidget.setGeometry(QtCore.QRect(5, 11, 581, 771))
        self.batting2TableWidget.setObjectName("batting2TableWidget")
        self.batting2TableWidget.setColumnCount(0)
        self.batting2TableWidget.setRowCount(0)
        self.tabWidget_2.addTab(self.batting2Tab, "")
        self.bowling2Tab = QtWidgets.QWidget()
        self.bowling2Tab.setObjectName("bowling2Tab")
        self.bowling2TableWidget = QtWidgets.QTableWidget(self.bowling2Tab)
        self.bowling2TableWidget.setGeometry(QtCore.QRect(5, 11, 591, 771))
        self.bowling2TableWidget.setObjectName("bowling2TableWidget")
        self.bowling2TableWidget.setColumnCount(0)
        self.bowling2TableWidget.setRowCount(0)
        self.tabWidget_2.addTab(self.bowling2Tab, "")
        self.scoreCardTab.addTab(self.scondInningTab, "")
        self.verticalLayout_5.addWidget(self.scoreCardTab)
        self.gridLayout_7.addWidget(self.scoreCardWidget, 0, 1, 1, 1)
        
        self.retranslateUi(matchPage)
        ## added by tafzeel
        self.button6.clicked.connect(self.onClick6)
        self.button5.clicked.connect(self.onClick5)
        self.button4.clicked.connect(self.onClick4)
        self.button3.clicked.connect(self.onClick3)
        self.button2.clicked.connect(self.onClick2)
        self.button1.clicked.connect(self.onClick1)
        self.button0.clicked.connect(self.onClick0)
        self.matchStatus.setText(tossStatus)
        self.team1Name.setText(self.team1.name)
        self.team2Name.setText(self.team2.name)
        self.swapBatsmanButton.clicked.connect(self.onClickSwapBatsman)
        self.updateTeamsScore(self.team1,self.team2)
        self.updateBatsman()
        self.updateBowler()
        #
        self.scoreCardTab.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(matchPage)
        matchPage.setTabOrder(self.scoreCardTab, self.isLegBye)
        matchPage.setTabOrder(self.isLegBye, self.isBye)
        matchPage.setTabOrder(self.isBye, self.isWide)
        matchPage.setTabOrder(self.isWide, self.isWicket)
        matchPage.setTabOrder(self.isWicket, self.swapBatsmanButton)
        matchPage.setTabOrder(self.swapBatsmanButton, self.isNoBall)
        matchPage.setTabOrder(self.isNoBall, self.button3)
        matchPage.setTabOrder(self.button3, self.button6)
        matchPage.setTabOrder(self.button6, self.button5)
        matchPage.setTabOrder(self.button5, self.button2)
        matchPage.setTabOrder(self.button2, self.buttonEndInnings)
        matchPage.setTabOrder(self.buttonEndInnings, self.button4)
        matchPage.setTabOrder(self.button4, self.button1)
        matchPage.setTabOrder(self.button1, self.button0)

    def retranslateUi(self, matchPage):
        _translate = QtCore.QCoreApplication.translate
        matchPage.setWindowTitle(_translate("matchPage", "Match"))
        self.matchStatus.setText(_translate("matchPage", "Team2 won the match by 6 wickets"))
        self.team1Name.setText(_translate("matchPage", "CSK"))
        self.team1Score.setText(_translate("matchPage", "145/8"))
        self.oversLabel1.setText(_translate("matchPage", "Overs :"))
        self.team1Over.setText(_translate("matchPage", "20"))
        self.team2Name.setText(_translate("matchPage", "RCB"))
        self.team2Score.setText(_translate("matchPage", "-/-"))
        self.oversLabel2.setText(_translate("matchPage", "Overs :"))
        self.team2Over.setText(_translate("matchPage", "-"))
        self.strikerName.setText(_translate("matchPage", "Dhoni"))
        self.strikerRunBall.setText(_translate("matchPage", "45(31)"))
        self.nonStrikerName.setText(_translate("matchPage", "DuPlesis"))
        self.nonStrikerRunBall.setText(_translate("matchPage", "76(62)"))
        self.thisOver.setText(_translate("matchPage", ""))
        self.bowlerName.setText(_translate("matchPage", "Steyn"))
        self.bowlerStats.setText(_translate("matchPage", "0/0  (0)"))
        self.isLegBye.setText(_translate("matchPage", "Leg Byes"))
        self.isBye.setText(_translate("matchPage", "Byes"))
        self.isWide.setText(_translate("matchPage", "Wide"))
        self.isWicket.setText(_translate("matchPage", "Wicket"))
        self.isNoBall.setText(_translate("matchPage", "No Ball"))
        self.swapBatsmanButton.setText(_translate("matchPage", "Swap Batsman"))
        self.applyDLButton.setText(_translate("matchPage", "Apply DL"))
        self.endMatchButton.setText(_translate("matchPage", "End Match"))
        self.button3.setText(_translate("matchPage", "3"))
        self.button6.setText(_translate("matchPage", "6"))
        self.button5.setText(_translate("matchPage", "5"))
        self.button2.setText(_translate("matchPage", "2"))
        self.buttonEndInnings.setText(_translate("matchPage", "End Innings"))
        self.button4.setText(_translate("matchPage", "4"))
        self.button1.setText(_translate("matchPage", "1"))
        self.button0.setText(_translate("matchPage", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.batting1Tab), _translate("matchPage", "Batting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bowling1Tab), _translate("matchPage", "Bowling"))
        self.scoreCardTab.setTabText(self.scoreCardTab.indexOf(self.firstInningTab), _translate("matchPage", "1st Inning"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.batting2Tab), _translate("matchPage", "Batting"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.bowling2Tab), _translate("matchPage", "Bowling"))
        self.scoreCardTab.setTabText(self.scoreCardTab.indexOf(self.scondInningTab), _translate("matchPage", "2nd Inning"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    matchPage = QtWidgets.QWidget()
    ui = Ui_matchPage()
    team1 = ['CSK','MS Dhoni','MS Dhoni','Shane Watson','Faf Du Plesis','Suresh Raina', 'Ambati Rayudu','Kedar Jadhav','Dwayne Bravo','Ravindra Jadeja','Deepak Chahar', 'Shardul Thakur','Imran Tahir']
    team2 = ['RCB','Parthiv Patel','Virat Kohli','Parthiv Patel','AB De Villiers', 'Akshdeep Nath','Moeen Ali','Marcus Stoinis','Pawan Negi','Dale Steyn','Navdeep Saini','Yuzvendra Chahal','Umesh Yadav']
    toss = ['CSK','Feild First',10]
    ui.setupUi(matchPage,toss[:],team1[:],team2[:])
    matchPage.show()
    sys.exit(app.exec_())

