import ui
import net
import chat
import background


class MapListItem(ui.ListBoxEx.Item):
	def __init__(self, map_idx, text):
		ui.ListBoxEx.Item.__init__(self)
		self.map_idx = map_idx
		self.text = text
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetText(text)
		self.textLine.SetPosition(5, 0)
		self.textLine.Show()

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetMapIndex(self):
		return self.map_idx


class InstanceBoardWindow(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.isLoaded = 0
		self.contentBoard = None
		self.mapListBox = None
		self.selectedMapIndex = 0

		# Map database matching the quest
		self.mapData = {
			1: "Map A1 - Jinno",
			3: "Map A3 - Chunjo",
			21: "Map B1 - Yongbi",
			23: "Map B3 - Bakra",
			41: "Map C1 - Imha",
			43: "Map C3 - Bokjung",
			61: "Snow Map",
			62: "Flame Dungeon",
			63: "Desert",
			64: "Three Way",
			65: "Milgyo",
			66: "Devil Tower",
		}

		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def __LoadWindow(self):
		print("InstanceBoardWindow: Loading UI...")
		if self.isLoaded == 1:
			return
		self.isLoaded = 1

		# Main Board Settings - Make taller for map list
		self.SetSize(350, 400)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName("Instance Manager")
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		# Content Background (Dark area)
		self.contentBoard = ui.ThinBoard()
		self.contentBoard.SetParent(self)
		self.contentBoard.SetPosition(15, 40)
		self.contentBoard.SetSize(320, 310)
		self.contentBoard.Show()

		# Header Text
		self.headerText = ui.TextLine()
		self.headerText.SetParent(self.contentBoard)
		self.headerText.SetPosition(160, 15)
		self.headerText.SetHorizontalAlignCenter()
		self.headerText.SetText("|cffFFC125Instance Manager|r")
		self.headerText.SetOutline()
		self.headerText.Show()

		# Status Text
		self.instanceStatus = ui.TextLine()
		self.instanceStatus.SetParent(self.contentBoard)
		self.instanceStatus.SetPosition(160, 35)
		self.instanceStatus.SetHorizontalAlignCenter()
		self.instanceStatus.SetText("")
		self.instanceStatus.SetOutline()
		self.instanceStatus.Show()

		# Map selection label
		self.mapLabel = ui.TextLine()
		self.mapLabel.SetParent(self.contentBoard)
		self.mapLabel.SetPosition(20, 80)
		self.mapLabel.SetText("|cffFFD700Select Map:|r")
		self.mapLabel.SetOutline()
		self.mapLabel.Show()

		# Map list box
		self.__CreateMapListBox()

		# Buttons
		self.__CreateActionButtons()

	def __CreateMapListBox(self):
		# ListBox for map selection
		self.mapListBox = ui.ListBoxEx()
		self.mapListBox.SetParent(self.contentBoard)
		self.mapListBox.SetPosition(20, 100)
		self.mapListBox.SetSize(280, 150)
		self.mapListBox.Show()

		# Populate with maps
		for map_idx in sorted(self.mapData.keys()):
			item = MapListItem(map_idx, self.mapData[map_idx])
			self.mapListBox.AppendItem(item)

	def __CreateActionButtons(self):
		# Warp to Lobby button
		self.warpToLobbyButton = ui.Button()
		self.warpToLobbyButton.SetParent(self.contentBoard)
		self.warpToLobbyButton.SetPosition(110, 100)
		self.warpToLobbyButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.warpToLobbyButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.warpToLobbyButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.warpToLobbyButton.SetText("Warp to Lobby")
		self.warpToLobbyButton.SetEvent(ui.__mem_func__(self.OnWarpToLobby))
		self.warpToLobbyButton.Hide()

		# Create Instance button (for selected map)
		self.createButton = ui.Button()
		self.createButton.SetParent(self.contentBoard)
		self.createButton.SetPosition(110, 260)
		self.createButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.createButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.createButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.createButton.SetText("Create Instance")
		self.createButton.SetEvent(ui.__mem_func__(self.OnCreateInstance))
		self.createButton.Hide()

		# Exit Instance button
		self.exitButton = ui.Button()
		self.exitButton.SetParent(self.contentBoard)
		self.exitButton.SetPosition(110, 100)
		self.exitButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.exitButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.exitButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.exitButton.SetText("Exit Instance")
		self.exitButton.SetEvent(ui.__mem_func__(self.OnExitInstance))
		self.exitButton.Hide()

	def OnCreateInstance(self):
		# Get selected item
		selected_item = self.mapListBox.GetSelectedItem()
		if not selected_item:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Please select a map first!")
			return

		# Get the map index from the selected item
		map_idx = selected_item.GetMapIndex()

		chat.AppendChat(chat.CHAT_TYPE_INFO, "Creating instance of %s..." % self.mapData[map_idx])

		# Send chat command for quest to intercept
		net.SendChatPacket("/instance_create %d" % map_idx)

		self.Close()

	def Open(self):
		# Get map index directly from background
		map_index = background.GetMapIndex()

		# If 0, map not loaded yet - show error and don't open UI
		if map_index == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Map not loaded yet, please try again in a moment")
			return

		chat.AppendChat(chat.CHAT_TYPE_INFO, "[DEBUG] UI Opening - Map Index: %d" % map_index)

		# STATE 1: Inside instance (map >= 10000) - Show exit button only
		if map_index >= 10000:
			self.headerText.SetText("|cff00FF00Instance Active|r")
			self.instanceStatus.SetText("|cffF5DEB3Map Index: %d|r" % map_index)

			# Hide everything except exit button
			self.mapLabel.Hide()
			self.mapListBox.Hide()
			self.createButton.Hide()
			self.warpToLobbyButton.Hide()
			self.exitButton.Show()

		# STATE 2: On lobby (map == 9999) - Show map selection only
		elif map_index == 9999:
			self.headerText.SetText("|cffFFC125Instance Lobby|r")
			self.instanceStatus.SetText("|cffFFD700Select a map to create instance|r")

			# Show map selection, hide other buttons
			self.mapLabel.Show()
			self.mapListBox.Show()
			self.createButton.Show()
			self.warpToLobbyButton.Hide()
			self.exitButton.Hide()

		# STATE 3: Normal maps - Show warp to lobby button only
		else:
			self.headerText.SetText("|cffFFC125Instance Manager|r")
			self.instanceStatus.SetText("|cffFFD700Warp to lobby to create instances|r")

			# Show warp button only
			self.mapLabel.Hide()
			self.mapListBox.Hide()
			self.createButton.Hide()
			self.warpToLobbyButton.Show()
			self.exitButton.Hide()

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def OnWarpToLobby(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Warping to instance lobby...")

		# Send chat command for quest to intercept
		net.SendChatPacket("/instance_lobby")

		self.Close()

	def OnExitInstance(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Exiting instance...")

		# Send chat command for quest to intercept
		net.SendChatPacket("/instance_exit")

		self.Close()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
