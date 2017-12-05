#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Love"
Website = "https://www.twitch.tv/pedromdevterceiro"
Description = "How much do you love someone?"
Creator = "PedroMDevTerceiro"
Version = "1.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
m_Response = ""
m_Command = "!love"
m_CooldownSeconds = 10
m_CommandInfo = ""

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
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
	command = data.GetParam(0)
	display_user_name = Parent.GetDisplayName(data.User)
	user = data.Message.replace(command, "").strip()
	streamer = Parent.GetChannelName()
	rng = Parent.GetRandom(1, 100)
	if data.IsChatMessage():
		if  command.lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command):
			if user == "":
				m_Response = "Align the stars and seek the guidance of the Love Meter with \"!love BabyRage \""
			elif user.lower() == streamer.lower():
				m_Response = "The love " + display_user_name + " has for our beloved Dear Leader " + streamer + " transcends all"
			else:
				m_Response = "There's " + str(rng) + "% riyuuLove between " + display_user_name + " and " + user
			Parent.SendTwitchMessage(m_Response)
	return