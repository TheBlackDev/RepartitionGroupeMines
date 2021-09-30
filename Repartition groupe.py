import time
import numpy as np
import copy as cp
import random as rd
import csv

# ------------ UTILITIES BEGIN ------------

def load_student_wishes(file_name):
    res=[]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            row.append(-1)
            res.append(row)
    res = np.array(res, dtype=np.int32)
    return res

def load_remaining_subjects(file_name):
    res=[]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            row.append(-1)
            res.append(row)
    res = np.array(res, dtype=np.int32)
    return res

def generate_blank_subject_table(numberofsubjects, nbmaxparsujet):
    a = np.zeros((numberofsubjects, 3), dtype=np.uint8)
    a[::, 0] = np.arange(0, numberofsubjects)
    a[::, 2] = nbmaxparsujet
    return a

def save_attributed_subject(attributions, file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in attributions:
            writer.writerow(line)
            
def save_rejected_students(attributions, file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in attributions[attributions[::, -1]==-1]:
            writer.writerow(line)
            
def save_remaining_subjects(remaining_subjects, file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in remaining_subjects:
            writer.writerow(line)
            
def save_group_composition(attributions, projects, file_name):
    a = []
    taille_max = int(max(projects[::, 2]))+1
    for project in projects:
        b = [-2]*taille_max #-2 signifie place inatribuable, -1 inatribué et sinon c l'id du gars en question
        b[0] = -3 #valeur temporaire on remplace par id projet après
        b[1:project[2]+1] = [-1]*project[2]
        a.append(b)
    for eleve in attributions:
        if(eleve[-1]!=-1):
            i = eleve[-1]
            j = -1
            for k in range(len(a[i])):
                if(a[i][k] == -1):
                    j=k
                    break
            a[i][j] = eleve[0]
    a=np.array(a, dtype=np.int32)
    a[::, 0] = np.arange(a.shape[0])
    
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for line in a:
            writer.writerow(line)
    
    
        
    
    
# ------------ UTILITIES END ------------


def round(n, table_sujet, table_eleve):
    nb_sujets = len(table_sujet)
    studentWishingSubject = [[] for i in range(nb_sujets)]
    for eleve in table_eleve:
        if(eleve[-1]==-1):
            studentWishingSubject[eleve[n]].append(eleve[0])
        
    for i in range(nb_sujets):        
        if((len(studentWishingSubject[i])+table_sujet[i, 1])<=table_sujet[i, 2] and 0<len(studentWishingSubject[i])):
            for eleve in studentWishingSubject[i]:
                table_eleve[eleve][-1] = i
                table_sujet[i,1] += 1
        
        
              
        elif(table_sujet[i, 2]<(len(studentWishingSubject[i])+table_sujet[i, 1]) and (table_sujet[i, 1]<table_sujet[i, 2])):
            allowed = []
            for j in range (table_sujet[i, 2]-table_sujet[i, 1]):
                allowed.append(rd.randint(0, len(studentWishingSubject[j])-1)) #-1 car la borne sup est incluse c'est mal fait...
            for j in allowed:
                table_eleve[j][4] = i
                table_sujet[i, 1] += 1
    return (table_sujet, table_eleve)
               
wishes = load_student_wishes('./exemple/voeux.csv')
subjects = generate_blank_subject_table(24, 5) # col0 = id_sujet | col1 = nb_actuel | col2 = nb_max

number_of_round = wishes.shape[1]-2
       
         
for i in range(1, number_of_round+1):
    subjects, wishes = round(i, subjects, wishes)
    
save_attributed_subject(wishes, './exemple/attributed-generated.csv')
save_rejected_students(wishes, './exemple/rejected-generated.csv')
save_remaining_subjects(subjects, './exemple/subjects-generated.csv')
save_group_composition(wishes, subjects, './exemple/groups-generated.csv')
    