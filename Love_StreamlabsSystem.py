#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import json
import os
import hashlib
import _sqlite3
from _sqlite3 import *

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Love"
Website = "https://www.twitch.tv/pedromdevterceiro"
Description = "How much do you love someone?"
Creator = "PedroMDevTerceiro"
Version = "1.0.1.0"

#---------------------------------------
# Set paths
#---------------------------------------
dirPath = os.path.dirname(os.path.realpath(__file__))
settingsPath = os.path.join(dirPath, "settings.json")
databasePath = os.path.join(dirPath, "love.s3db")

#---------------------------------------
# Set Variables
#---------------------------------------
m_Empty_Love_Response = "Align the stars and seek the guidance of the Love Meter with \"!love BabyRage \""
m_Love_Streamer_Response = "The love $fromuser has for our beloved Dear Leader $streamername transcends all"
m_Love_Someone_Response = "There's $percentage% :heart: between $fromuser and $beloved"
m_CooldownSeconds = 10
m_UseSavedLovePercentage = False
m_Command = "!love"

#---------------------------------------
# Util Functions
#---------------------------------------
def UpdateVariablesFromJson(jsonData):
	global ScriptName, m_Empty_Love_Response, m_Love_Streamer_Response, m_Love_Someone_Response, m_CooldownSeconds, m_UseSavedLovePercentage
	Parent.Log(ScriptName, "Updating Variables...")
	m_Empty_Love_Response = jsonData["empty_love_response"]
	m_Love_Streamer_Response = jsonData["love_streamer_response"]
	m_Love_Someone_Response = jsonData["love_someone_response"]
	m_CooldownSeconds = jsonData["cd"]
	if "save_love_percentage" not in jsonData:
		m_UseSavedLovePercentage = False
	else:
		m_UseSavedLovePercentage = jsonData["save_love_percentage"]
	return

def ReloadSettings(jsonData):
	global ScriptName, m_Command, m_CooldownSeconds
	UpdateVariablesFromJson(json.loads(jsonData))
	Parent.AddCooldown(ScriptName, m_Command, m_CooldownSeconds)
	Parent.Log(ScriptName, "Settings has been updated")
	return

def CreateDatabaseIfNotExists():
	global ScriptName, databasePath
	if not os.path.exists(databasePath):
		Parent.Log(ScriptName, "Creating database...")
		con = _sqlite3.connect(databasePath)
		con.execute('''CREATE TABLE loves
			(
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			key NVARCHAR(64) NOT NULL,
			percentage INTEGER NOT NULL
			)''')
		con.commit()
		con.close()
	return

def GetLoveKey(fromuser, beloved):
	return hashlib.sha256(fromuser.lower() + beloved.lower()).hexdigest()

def GetLovePercentageFromDatabase(fromuser, beloved):
	global ScriptName, databasePath
	loveKey = GetLoveKey(fromuser, beloved)
	con = _sqlite3.connect(databasePath)
	cur = con.cursor()
	cur.execute("SELECT percentage FROM loves WHERE key=?", (loveKey,))
	row = cur.fetchone()
	cur.close()
	con.close()
	if row is None:
		return -1
	return row[0]

def UpdateLovePercentage(fromuser, beloved, percentage):
	global ScriptName, databasePath
	loveKey = GetLoveKey(fromuser, beloved)
	con = _sqlite3.connect(databasePath)
	cur = con.cursor()
	cur.execute("INSERT INTO loves(key, percentage) VALUES(?, ?)", (loveKey, percentage,))
	con.commit()
	cur.close()
	con.close()
	return

def GetLovePercentage(fromuser, beloved):
	global m_UseSavedLovePercentage
	rndPercentage = Parent.GetRandom(0, 100)
	if m_UseSavedLovePercentage:
		percentage = GetLovePercentageFromDatabase(fromuser, beloved)
		if percentage == -1:
			percentage = rndPercentage
			UpdateLovePercentage(fromuser, beloved, percentage)
		return percentage
	return rndPercentage

#---------------------------------------
# [Required] Initialize Data (Only called on Load)
#---------------------------------------
def Init():
	global ScriptName, dirPath, settingsPath, m_Command
	Parent.Log(ScriptName, "Initializing script...")
	CreateDatabaseIfNotExists()
	if os.path.isfile(settingsPath):
		Parent.Log(ScriptName, "Getting settings from file...")
		with open(settingsPath) as jsonSettingsFile:
			jsonData = json.loads(jsonSettingsFile.read().decode("utf-8-sig").encode("utf-8"))
			UpdateVariablesFromJson(jsonData)
	return

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
	return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
	global ScriptName, m_Command, m_Empty_Love_Response, m_Love_Streamer_Response, m_Love_Someone_Response, m_CooldownSeconds
	command = data.GetParam(0)
	display_user_name = Parent.GetDisplayName(data.User)
	user = data.Message.replace(command, "").strip()
	streamer = Parent.GetDisplayName(Parent.GetChannelName())
	if data.IsChatMessage():
		if  command.lower() == m_Command and not Parent.IsOnCooldown(ScriptName, m_Command):
			if user == "":
				m_Response = m_Empty_Love_Response.replace("$fromuser", display_user_name)
			elif user.lower() == streamer.lower():
				m_Response = m_Love_Streamer_Response.replace("$fromuser", display_user_name).replace("$streamername", streamer)
			else:
				rng = GetLovePercentage(data.User.lower(), user.lower())
				m_Response = m_Love_Someone_Response.replace("$percentage", str(rng)).replace("$fromuser", display_user_name).replace("$beloved", user)
			Parent.SendTwitchMessage(m_Response)
			Parent.AddCooldown(ScriptName, m_Command, m_CooldownSeconds)
			Parent.Log(ScriptName, "Command Response: " + m_Response)
	return