from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8", newline="") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?(?:доб\.?)\s*(\d+)\)?)?"
)

new_contacts = []

for contact in contacts_list:
    full_name = " ".join(contact[:3]).split()
    lastname = full_name[0] if len(full_name) > 0 else ""
    firstname = full_name[1] if len(full_name) > 1 else ""
    surname = full_name[2] if len(full_name) > 2 else ""

    organization = contact[3]
    position = contact[4]
    phone = contact[5]
    email = contact[6]

    phone = phone_pattern.sub(
        lambda m: f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
        + (f" доб.{m.group(6)}" if m.group(6) else ""),
        phone
    )

    new_contacts.append([
        lastname,
        firstname,
        surname,
        organization,
        position,
        phone,
        email
    ])

merged_contacts = {}

header = new_contacts[0]

for contact in new_contacts[1:]:
    key = (contact[0], contact[1])

    if key not in merged_contacts:
        merged_contacts[key] = contact
    else:
        for i in range(len(contact)):
            if merged_contacts[key][i] == "" and contact[i] != "":
                merged_contacts[key][i] = contact[i]

contacts_list = [header] + list(merged_contacts.values())

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(contacts_list)