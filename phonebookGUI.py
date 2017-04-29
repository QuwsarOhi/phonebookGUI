# Simpple Python contact app
# Python 3, PyGTK+ 3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class Contact:
    ''' Stores data in dictionary, import data from file, export data to file
        add, remove contact'''

    def __init__(self):
        self.name_to_number = dict()

    def addContact(self, name, number):
        if name not in self.name_to_number:
            self.name_to_number[name] = number
            return True
        return False

    def exportFile(self, fileName):
        with open(fileName, 'w') as File:
            for key in self.name_to_number:
                File.write("{0} {1}\n".format(key, self.name_to_number[key]))

    def importFile(self, fileName):
        try:
            iFile = open(fileName, 'r')
            while True:
                s = iFile.readline()
                if s == '':
                    break
                a, b = s.strip().split(' ')
                self.name_to_number[a] = b
                self.number_to_name[b] = a
        
            iFile.close()
        except:
            pass

    def passIterator(self):
        return self.name_to_number.items()
        
    def removeContact(self, name, number):
        if name in self.name_to_number:
            del self.name_to_number[name]

class ContactEntry(Gtk.Window):
	'''Add contact window'''
	
	def __init__(self, contactObj, contact_list):
		Gtk.Window.__init__(self, title='Add Contact')
		self.set_border_width(2)
		self.contact_list = contact_list
		self.set_default_size(300, 100)
		
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)
		
		self.nameEntry = Gtk.Entry()
		self.nameEntry.set_text('Name')
		vbox.pack_start(self.nameEntry, True, True, 6)

		self.numberEntry = Gtk.Entry()
		self.numberEntry.set_text('Contact')
		vbox.pack_start(self.numberEntry, True, True, 6)		
		
		self.button = Gtk.Button(label='Add')
		self.button.connect("clicked", self.on_button_clicked)
		vbox.pack_start(self.button, True, True, 1)
		
	def on_button_clicked(self, widget):
		name = self.nameEntry.get_text()
		number = self.numberEntry.get_text()
		if name != 'Name' and number != 'number':
			if contactObj.addContact(name, number):
				tmp = (name, number)
				self.contact_list.append(tmp)	# Appending to ContactView's contact_list
		self.destroy()							# Destroy by pressing 'ADD'

class ContactView(Gtk.Window):
	'''The main window '''
	
	def __init__(self, contactObj):
		Gtk.Window.__init__(self, title="Phonebook")
		self.connect("delete-event", Gtk.main_quit)
		self.set_border_width(5)
		self.set_default_size(250, 200)
		self.contactObj = contactObj
		
		# Generating ListStore for contact data
		self.contact_list = Gtk.ListStore(str, str)
		it = contactObj.passIterator()
		for x, y in it:
			tmp = (x, y)
			self.contact_list.append(tmp)
		
		# Giving The tree view the viweing table model (Column Titles and data)
		self.contact_treeview = Gtk.TreeView(self.contact_list)
		for i, col_title in enumerate(['Name', 'Number']):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(col_title, renderer, text=i)
			# Enabling sort feature
			column.set_sort_column_id(0)
			
			self.contact_treeview.append_column(column)
	
		# Setting to scrollable
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.add(self.contact_treeview)
		scrolled_window.set_min_content_height(200)
		
		box1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.add(box1)
		box1.pack_start(scrolled_window, True, True, 1)
		
		# Add button in box
		addButton = Gtk.Button()
		addButton.set_label('Add')
		addButton.connect("clicked", self.addContact)
		box1.pack_start(addButton, True, True, 1)
		
		# Delete button in box
		deleteButton = Gtk.Button()
		deleteButton.set_label('Delete')
		deleteButton.connect("clicked", self.deleteContact)
		box1.pack_start(deleteButton, True, True, 1)
		
		
	def addContact(self, widget):
		test = ContactEntry(contactObj, self.contact_list)
		test.show_all()
	
	def deleteContact(self, widget):
		selection = self.contact_treeview.get_selection()
		model, paths = selection.get_selected_rows()
		contactObj.removeContact(model[paths][0], model[paths][1])
		# Removing contact from display (TreeView)
		for path in paths:
			iter = model.get_iter(path)
			model.remove(iter)
		
		

if __name__ == '__main__':
	contactObj = Contact()
	contactObj.importFile('data.txt')		# Import contacts from file

	win = ContactView(contactObj)
	win.show_all()
	Gtk.main()
	contactObj.exportFile('data.txt')		# Export contacts to file
