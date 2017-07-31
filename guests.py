import csv
from mongo import db, auth

auth
guestlist = db['guestlist']


def add_guest(name, twitter='', urls=[]):
  entry = {
          'name': name,
          'twitter': twitter,
          'urls': urls
          }
  return guestlist.insert_one(entry)

def add_guests_csv(csvfile):
    with open(csvfile) as f:
        reader = csv.reader(f)
        for guest in reader:
            add_guest(guest[0], guest[1])
