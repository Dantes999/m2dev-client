import ui
import net
import chat
import app

class InstanceItem(ui.ListBoxEx.Item):
	def __init__(self, id, text):
		ui.ListBoxEx.Item.__init__(self)
		self.id = id
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetPosition(0, 0)
		self.textLine.SetText(text)
		self.textLine.Show()

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

class InstanceManagerWindow(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.isLoaded = 0
		self.instanceList = []
		self.listbox = None
		self.refreshBtn = None
		self.closeInstanceBtn = None
		
		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1

		self.SetSize(400, 300)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName("GM Instance Manager")
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		# ListBox
		self.listbox = ui.ListBoxEx()
		self.listbox.SetParent(self)
		self.listbox.SetPosition(10, 35)
		self.listbox.SetSize(380, 220)
		self.listbox.SetViewItemCount(13)
		self.listbox.SetItemSize(380, 16)
		self.listbox.SetItemStep(16)
		self.listbox.Show()

		# Refresh Button
		self.refreshBtn = ui.Button()
		self.refreshBtn.SetParent(self)
		self.refreshBtn.SetPosition(10, 265)
		self.refreshBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.refreshBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.refreshBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.refreshBtn.SetText("Refresh List")
		self.refreshBtn.SetEvent(ui.__mem_func__(self.RefreshList))
		self.refreshBtn.Show()

		# Close Instance Button
		self.closeInstanceBtn = ui.Button()
		self.closeInstanceBtn.SetParent(self)
		self.closeInstanceBtn.SetPosition(200, 265)
		self.closeInstanceBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.closeInstanceBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.closeInstanceBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.closeInstanceBtn.SetText("Close Instance")
		self.closeInstanceBtn.SetEvent(ui.__mem_func__(self.CloseInstance))
		self.closeInstanceBtn.Show()

	def ClearList(self):
		self.listbox.RemoveAllItems()
		self.instanceList = []

	def AddInstance(self, id, map_index, duration, player_names):
		text = "ID: %s | Map: %s | Time: %sm | Players: %s" % (id, map_index, duration, player_names)
		item = InstanceItem(id, text)
		item.SetSize(380, 16)
		self.listbox.AppendItem(item)
		self.instanceList.append(item)

	def RefreshList(self):
		net.SendChatPacket("/instance_list")

	def CloseInstance(self):
		item = self.listbox.GetSelectedItem()
		if not item:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Select an instance first.")
			return
		
		net.SendChatPacket("/instance_close %s" % item.id)
		# We will wait for the refresh from server or manual refresh
		# self.RefreshList() 

	def Open(self):
		if not self.IsShow():
			self.Show()
			self.SetTop()
			self.RefreshList()

	def Close(self):
		self.Hide()

	def Toggle(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

	def OnPressEscapeKey(self):
		self.Close()
		return True
