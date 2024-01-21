import time

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QMessageBox, \
    QComboBox, QCheckBox, QInputDialog
from PyQt5.QtCore import Qt
from functools import partial
from pbContent import contactListData, contact

contactsListData = contactListData()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        # display list variable for window
        self.filteredContacts = []
        # read from data item and filter contacts
        self.filterContactsListByTextAndTags()
        # create window
        self.setWindowTitle('My Phonebook')
        #
        mainWidget = QWidget()
        #
        mainWidget.setLayout(self.createMainDisplayLayout())
        #
        self.setCentralWidget(mainWidget)
        #
        self.show()

    def createMainDisplayLayout(self) -> QHBoxLayout:
        # create the search menu title and add to main widget
        searchMenuLayout = QVBoxLayout()
        #
        quitButton = QPushButton('Quit')
        quitButton.pressed.connect(self.quitApp)
        #
        searchMenuLayout.addWidget(quitButton)
        #
        searchContactTitle = QLineEdit('Search Contacts:')
        searchContactTitle.setDisabled(True)
        #
        searchMenuLayout.addWidget(searchContactTitle)
        # add filter text and search button
        textFilterLayout = QHBoxLayout()
        #
        self.textFilterInputItem = QLineEdit(contactsListData.textFilter)
        #
        textFilterButton = QPushButton('Search')
        textFilterButton.pressed.connect(self.setTextFilter)
        #
        textFilterLayout.addWidget(self.textFilterInputItem)
        textFilterLayout.addWidget(textFilterButton)
        #
        searchMenuLayout.addLayout(textFilterLayout)
        #
        addContactButton = QPushButton('Create New Contact')
        addContactButton.pressed.connect(self.switchToEditContactWindow)
        #
        searchMenuLayout.addWidget(addContactButton)
        # search by tag line
        searchByTagItemsLayout = QHBoxLayout()
        # if filter isnt '' the mark filter is on
        isTagFilter = QCheckBox()
        if not contactsListData.tagFilter == '':
            isTagFilter.setChecked(True)
        isTagFilter.setDisabled(True)
        #
        searchByTagItemsLayout.addWidget(isTagFilter)
        #
        self.searchByTag = QComboBox()
        for tag in contactsListData.contactListTags:
            self.searchByTag.addItem(tag)
        if contactsListData.tagFilter in contactsListData.contactListTags:
            self.searchByTag.setCurrentText(contactsListData.tagFilter)
        #
        searchByTagButton = QPushButton('Search tagged')
        searchByTagButton.pressed.connect(self.setTagFilter)
        #
        clearTagButton = QPushButton('Clear tag')
        clearTagButton.pressed.connect(self.clearTagFilter)
        #
        searchByTagItemsLayout.addWidget(self.searchByTag)
        searchByTagItemsLayout.addWidget(searchByTagButton)
        searchByTagItemsLayout.addWidget(clearTagButton)
        #
        searchMenuLayout.addLayout(searchByTagItemsLayout)
        #
        tagButtonsLayout = QHBoxLayout()
        #
        deleteTagButton = QPushButton('Delete Tag')
        deleteTagButton.pressed.connect(self.deleteTag)
        #
        addTagButton = QPushButton('Create New Tag')
        addTagButton.pressed.connect(self.CreateTag)
        #
        tagButtonsLayout.addWidget(deleteTagButton)
        tagButtonsLayout.addWidget(addTagButton)
        #
        searchMenuLayout.addLayout(tagButtonsLayout)
        # set contact list title
        contactListLineLayout = QHBoxLayout()
        #
        contactListTitle = QLineEdit('Contacts:')
        contactListTitle.setDisabled(True)
        #
        deleteContactListButton = QPushButton('X')
        deleteContactListButton.pressed.connect(self.deleteContactList)
        #
        contactListLineLayout.addWidget(contactListTitle)
        contactListLineLayout.addWidget(deleteContactListButton)
        #
        searchMenuLayout.addLayout(contactListLineLayout)
        #
        contactListLayout = QVBoxLayout()
        # if the data file has no contacts
        if len(contactsListData.contactListPeople) == 0:
            contactListEmpty = QLineEdit('Contacts list is empty')
            contactListEmpty.setDisabled(True)
            contactListLayout.addWidget(contactListEmpty)
        # if all contacts are filtered - bugged
        # this is one of the debug points, the "weaker one" (filter to empty list)
        elif len(self.filteredContacts) == 0:
            contactListFiltered = QLineEdit('All contacts were filtered')
            contactListFiltered.setDisabled(True)
            contactListLayout.addWidget(contactListFiltered)
        #
        else:
            # if the file is not empty and not all contacts are filtered from view
            for person in self.filteredContacts:
                personButtonsLayout = QHBoxLayout()
                #
                personButton = QPushButton(person.firstName + ' ' + person.lastName)
                personButton.pressed.connect(partial(self.switchToEditContactWindow, person))
                #
                deletePersonButton = QPushButton('X')
                deletePersonButton.pressed.connect(partial(self.deleteContact, person))
                #
                personButtonsLayout.addWidget(personButton)
                personButtonsLayout.addWidget(deletePersonButton)
                #
                contactListLayout.addLayout(personButtonsLayout)
                #
        searchMenuLayout.addLayout(contactListLayout)
        return searchMenuLayout

    def quitApp(self):
        raise SystemExit

    def deleteTag(self):
        contactsListData.deleteTag(self.searchByTag.currentText())
        self.close()

    def CreateTag(self):
        tagName, tagInputTextBox = QInputDialog.getText(self, 'Enter Tag', 'Enter Tag Name:')
        if tagInputTextBox:
            contactsListData.createTag(tagName)
            self.close()

    def clearTagFilter(self):
        contactsListData.tagFilter = ''
        self.close()

    def deleteContact(self, curContact: contact):
        contactsListData.deleteContact(curContact)
        self.close()

    # this method doesnt trigger the close event unless debugged at line event.accept() - note you are in mainwindow class no editwindow class
    def deleteContactList(self):
        try:
            contactsListData.deleteContactList()
        except Exception as e:
            print('failed to delete list!,', e)
        else:
            contactsListData.__init__()

        self.close()

    def setTextFilter(self):
        contactsListData.textFilter = self.textFilterInputItem.text().lower()
        self.close()

    def filterContactsListByTextAndTags(self):
        # filter by text
        for person in contactsListData.contactListPeople:
            fullName = (person.firstName + ' ' + person.lastName).lower()
            if fullName.startswith(contactsListData.textFilter):
                self.filteredContacts.append(person)
        # filter by tag
        if not contactsListData.tagFilter == '':
            filteredContactsCopy = self.filteredContacts.copy()
            for person in filteredContactsCopy:
                if contactsListData.tagFilter not in person.tags:
                    self.filteredContacts.remove(person)

    def setTagFilter(self):
        contactsListData.tagFilter = self.searchByTag.currentText()
        self.close()

    def switchToEditContactWindow(self, curContact: contact = contact()):
        # bug fix #
        # issue trying to discard selected tags when cancelling creation - setting manually
        if curContact.firstName == '' and curContact.lastName == '' and curContact.phoneNumber == '':
            curContact.tags = []
        editContactWindow = EditContactWindow(curContact)
        self.destroy(True)

    def closeEvent(self, event):
        window = MainWindow()
        time.sleep(2)
        event.accept()


class EditContactWindow(QMainWindow):

    def __init__(self, curContact: contact):
        super().__init__()

        # create window
        self.setWindowTitle(f'Contact Details for: {curContact.firstName} {curContact.lastName}')
        #
        contactWidget = QWidget()
        #
        contactMenuLayout = QHBoxLayout()
        #
        contactWidget.setLayout(contactMenuLayout)
        #
        self.setCentralWidget(contactWidget)
        # creating the search menu and add to display
        mainContactLayout = self.createDisplayLayout(curContact)
        #
        contactMenuLayout.addLayout(mainContactLayout)
        #
        self.show()

    def createDisplayLayout(self, curContact: contact) -> QVBoxLayout:
        editContactLayout = QVBoxLayout()
        #
        firstnameInputLayout = QHBoxLayout()
        #
        firstnameTitle = QLineEdit('Firstname:')
        firstnameTitle.setDisabled(True)
        #
        self.firstnameTextbox = QLineEdit(curContact.firstName)
        #
        firstnameInputLayout.addWidget(firstnameTitle)
        firstnameInputLayout.addWidget(self.firstnameTextbox)
        #
        editContactLayout.addLayout(firstnameInputLayout)
        #
        lastnameInputLayout = QHBoxLayout()
        #
        lastnameTitle = QLineEdit('Lastname:')
        lastnameTitle.setDisabled(True)
        #
        self.lastnameTextbox = QLineEdit(curContact.lastName)
        #
        lastnameInputLayout.addWidget(lastnameTitle)
        lastnameInputLayout.addWidget(self.lastnameTextbox)
        #
        editContactLayout.addLayout(lastnameInputLayout)
        #
        phoneInputLayout = QHBoxLayout()
        #
        phoneTitle = QLineEdit('Phone Number:')
        phoneTitle.setDisabled(True)
        #
        self.phoneTextbox = QLineEdit(curContact.phoneNumber)
        #
        phoneInputLayout.addWidget(phoneTitle)
        phoneInputLayout.addWidget(self.phoneTextbox)
        #
        editContactLayout.addLayout(phoneInputLayout)
        #
        tagLayout = QVBoxLayout()
        for tag in contactsListData.contactListTags:
            tagCheckbox = QCheckBox()
            #
            tagName = QLineEdit(tag)
            tagName.setDisabled(True)
            #
            current_tag = tag
            # when QCheckbox item clicked sends to trigger tags list event for curContact,
            tagCheckbox.stateChanged.connect(
                lambda state, t=current_tag: self.checkboxStateChange(state, t, curContact))
            # block signals so that showing current tags wont trigger double tag write to list
            if current_tag in curContact.tags:
                tagCheckbox.blockSignals(True)
                tagCheckbox.setChecked(True)
                tagCheckbox.blockSignals(False)
            #
            tagLayout.addWidget(tagName)
            tagLayout.addWidget(tagCheckbox)
            #
        editContactLayout.addLayout(tagLayout)
        #
        actionButtonsLayout = QHBoxLayout()
        #
        saveButton = QPushButton('Save')
        saveButton.pressed.connect(partial(self.saveAndClose, curContact))
        #
        backButton = QPushButton('Back')
        backButton.pressed.connect(self.dontSaveAndClose)
        #
        actionButtonsLayout.addWidget(saveButton)
        actionButtonsLayout.addWidget(backButton)
        #
        editContactLayout.addLayout(actionButtonsLayout)
        #
        return editContactLayout

    def checkboxStateChange(self, state, t, curContact):
        if state == 2:  # Checked state
            curContact.tags.append(t)
        else:  # Unchecked state
            curContact.tags.remove(t)

    def dontSaveAndClose(self):
        # close event did not trigger directly from button press
        self.close()

    def saveAndClose(self, curContact: contact):
        if curContact in contactsListData.contactListPeople:
            contactsListData.contactListPeople.remove(curContact)
        newContact = contact(self.firstnameTextbox.text(), self.lastnameTextbox.text(), self.phoneTextbox.text(),
                             curContact.tags)
        contactsListData.createContact(newContact)
        self.close()

    def closeEvent(self, event):
        window = MainWindow()
        event.accept()
