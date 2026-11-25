from get_lessons import get_lessons
from get_maquette import get_maquette_verDirect, get_maquette_verCompiled

def get_time_lessons(module_name):
    lessons = get_lessons(module_name)
    time_onLessons = {'cm':0, 'td':0, 'tp':0, 'contact_total':0}
    # travel the list to get each duration in minutes
    for lesson in lessons:
        if lesson['type_cours'] == 'CM':
            time_onLessons['cm'] += lesson['duree_minutes']
        elif lesson['type_cours'] == 'TD':
            time_onLessons['td'] += lesson['duree_minutes']
        elif lesson['type_cours'] == 'TP':
            time_onLessons['tp'] += lesson['duree_minutes']
        time_onLessons['contact_total'] += lesson['duree_minutes']

    # translation from minutes to hours
    for category in time_onLessons:
        time_onLessons[category] = time_onLessons[category] / 60

    return time_onLessons

def matching_lessons(module_name):
    maquette = get_maquette_verDirect(module_name)
    print("maquette : \n"+str(maquette))
    time_onLessons = get_time_lessons(module_name)
    print("actual time : \n"+str(time_onLessons)+"\n####")

module_nameTEST = "INFO732_IDU"
matching_lessons(module_nameTEST)