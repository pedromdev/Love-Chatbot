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

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Love"
Website = "https://www.twitch.tv/pedromdevterceiro"
Description = "How much do you love someone?"
Creator = "PedroMDevTerceiro"
Version = "1.0.0.0"

#---------------------------------------
# Set paths
#---------------------------------------
dirPath = os.path.dirname(os.path.realpath(__file__))
settingsPath = os.path.join(dirPath, "settings.json")

#---------------------------------------
# Set Variables
#---------------------------------------
m_Empty_Love_Response = "Align the stars and seek the guidance of the Love Meter with \"!love BabyRage \""
m_Love_Streamer_Response = "The love $fromuser has for our beloved Dear Leader $streamername transcends all"
m_Love_Someone_Response = "There's $percentage% :heart: between $fromuser and $beloved"
m_CooldownSeconds = 10
m_Command = "!love"

#---------------------------------------
# Util Functions
#---------------------------------------
def UpdateVariablesFromJson(jsonData):
	global ScriptName, m_Empty_Love_Response, m_Love_Streamer_Response, m_Love_Someone_Response, m_CooldownSeconds
	Parent.Log(ScriptName, "Updating Variables...")
	m_Empty_Love_Response = jsonData["empty_love_response"]
	m_Love_Streamer_Response = jsonData["love_streamer_response"]
	m_Love_Someone_Response = jsonData["love_someone_response"]
	m_CooldownSeconds = jsonData["cd"]
	return

def ReloadSettings(jsonData):
	global ScriptName, m_Command, m_CooldownSeconds
	UpdateVariablesFromJson(json.loads(jsonData))
	Parent.AddCooldown(ScriptName, m_Command, m_CooldownSeconds)
	Parent.Log(ScriptName, "Settings has been updated")
	return

#---------------------------------------
# [Required] Initialize Data (Only called on Load)
#---------------------------------------
def Init():
	global ScriptName, dirPath, settingsPath, m_Command
	Parent.Log(ScriptName, "Initializing script...")
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
	rng = Parent.GetRandom(1, 100)
	if data.IsChatMessage():
		if  command.lower() == m_Command and not Parent.IsOnCooldown(ScriptName, m_Command):
			if user == "":
				m_Response = m_Empty_Love_Response.replace("$fromuser", display_user_name)
			elif user.lower() == streamer.lower():
				m_Response = m_Love_Streamer_Response.replace("$fromuser", display_user_name).replace("$streamername", streamer)
			else:
				m_Response = m_Love_Someone_Response.replace("$percentage", str(rng)).replace("$fromuser", display_user_name).replace("$beloved", user)
			Parent.SendTwitchMessage(m_Response)
			Parent.AddCooldown(ScriptName, m_Command, m_CooldownSeconds)
			Parent.Log(ScriptName, "Command Response: " + m_Response)
	return