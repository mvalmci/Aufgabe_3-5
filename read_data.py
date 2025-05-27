import json

def load_person_data():
   
    file = open("data/person_db.json")
    person_data = json.load(file)

    return person_data


def get_person_list(person_data=None):
    person_data = load_person_data()
    person_list = []

    for person in person_data:
        person_list.append(person["firstname"] + ", " + person["lastname"])
        
    return person_list


def get_picture_path(person_data=None):
    person_data = load_person_data()
    picture_path = []

    for person in person_data:
        picture_path.append(person["picture_path"])
        
    return picture_path


def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""

    person_data = load_person_data()
    #print(suchstring)
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        print(eintrag)
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print()

            return eintrag
    else:
        return {}








if __name__ == "__main__":
    person_data = load_person_data()
    person_list = get_person_list(person_data)
    print(person_list)
    picture_path = get_picture_path(person_data)
    print(picture_path)