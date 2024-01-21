import os
import json

PB_FILE = './pb.json'


class contact:
    def __init__(self, firstName: str = '', lastName: str = '', phoneNumber: str = '', tags: list = []):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.tags = tags

    def toDict(self):
        return {
            "first_name": self.firstName,
            "last_name": self.lastName,
            "phone_number": self.phoneNumber,
            "tags": self.tags
        }


class contactListData:
    def __init__(self):
        self.contactListPeople: list[contact] = []
        self.contactListTags: list[str] = []

        if os.path.exists(PB_FILE):
            try :
                self.readContactsFile()
            except Exception as e:
                print('cant open file',e)

        self.textFilter=''
        self.tagFilter= ''

    def createContact(self, curContact: contact):
        self.contactListPeople.append(curContact)
        self.writeContactsFile()

    def deleteContact(self, curContact: contact):
        if curContact in self.contactListPeople:
            self.contactListPeople.remove(curContact)
            self.writeContactsFile()

    def deleteContactList(self):
        self.contactListPeople: list[contact] = []
        self.writeContactsFile()

    def createTag(self, curTag: str):
        self.contactListTags.append(curTag)
        self.writeContactsFile()

    def deleteTag(self, curTag: str):
        for person in self.contactListPeople:
            if curTag in person.tags:
                person.tags.remove(curTag)
        if curTag in self.contactListTags:
            self.contactListTags.remove(curTag)
        self.writeContactsFile()

    def readContactsFile(self):
        try:
            f = open(PB_FILE, 'r')
        except Exception as e:
            print('error!', e)
        else:
            contactListFile = json.load(f)
            contactsList = []
            for curContact in contactListFile['Contacts']:
                contactsList.append(contact(curContact['first_name'],curContact['last_name'],curContact['phone_number'],curContact['tags']))
            self.contactListPeople: list[contact] = contactsList
            self.contactListTags: list[str] = contactListFile['Tags']
        finally:
            f.close()

    def writeContactsFile(self):
        try:
            f = open(PB_FILE, 'w')
        except Exception as e:
            print('error!', e)
        else:
            contactsDictList=[curContact.toDict() for curContact in self.contactListPeople]
            contactListFile = {'Contacts': contactsDictList, 'Tags': self.contactListTags}
            json.dump(contactListFile, f, indent=4)
        finally:
            f.close()
