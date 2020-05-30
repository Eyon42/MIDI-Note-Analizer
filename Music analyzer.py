#!/usr/bin/env python
# coding: utf-8

# In[1]:


from mido import MidiFile, Message
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import csv


# Nota para exportar: eliminar las tracks de percusión

# In[2]:


#Individual track analisis

def get_note_list(track):
    notes = []
    for m in track:
        if m.type == 'note_on':
            notes.append(m.note)
    return notes


with open('Midi_notes.csv') as di:
    read = csv.DictReader(di)
    midi_note_dict = next(read)

    
def midiNum_to_note(num):
    if 20 < num < 128:
        return midi_note_dict[str(num)]
    else:
        return None
    
    
def count_notes(track):
    Track_note_list = get_note_list(track)
    n_counter = Counter(Track_note_list)
    return n_counter


# In[81]:


# Multi-track analisis and preparation

def det_song_range(track_counts):
    '''Determina las notas mas bajas y mas altas de un conjunto de cuentas de notas'''
    song_range = [[],[]]
    for i in range(0,len(track_counts)):
        song_range[0].append(min(track_counts[i].keys()))
        song_range[1].append(max(track_counts[i].keys()))
    return min(song_range[0]), max(song_range[1])+1


def fill_note_count_range(track_count, rmin, rmax):
    '''Esto se asegura de que esten todas las notas en el rango de la cancion,
    aunque dichas notas no se encuentren presentes'''
    for i in range(rmin, rmax):
            track_count[i] += 0   

            
def ordered_multiTrack_note_count(tracks):
    '''Entrega una lista de diccionarios ordenados con el rango completo de notas
    separado por pistas. Además, entrega el rango de la lista'''
    mT_ord_count = []
    track_counts = [Counter(get_note_list(track)) for track in tracks]
    r_min, r_max = det_song_range(track_counts)
    for track_c in track_counts:
        fill_note_count_range(track_c, r_min, r_max)
        mT_ord_count.append(OrderedDict(sorted(track_c.items())))
    return mT_ord_count, (r_min, r_max)

def plot_stacked_bars(indexes, values, colors):
    prev_bars = np.zeros(len(values[0]))
    for i in range(0, len(values)):
        plt.bar(indexes, values[i], width = 1, edgecolor = 'Black',
                linewidth=0.1, color=colors[i],
                bottom=prev_bars)
        prev_bars += np.array(values[i])


# In[82]:


#Plot function

def plot_tracks_note_quantity(tracks, track_names, title):
    count_to_plot, note_range = ordered_multiTrack_note_count(tracks)
    note_indexes = [midiNum_to_note(n) for n in range(*note_range)]
    note_lists = [[k for k in c.values()] for c in count_to_plot]
    max_note_amount = max(sum([np.array(i) for i in note_lists]))
    
    colors = [palette[3],palette[5],palette[2], palette[0], palette[1], palette[4], palette[6], palette[7]]
    
    plot_stacked_bars(note_indexes, note_lists, colors)

    plt.xlabel('Notes')
    plt.ylabel('Times played')
    plt.legend(track_names)
    plt.title(title)
    plt.ylim(0,max_note_amount*1.1)


# In[94]:


plt.style.use('ggplot')
palette = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
#palette from http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
plt.rcParams["figure.figsize"] = (30,30)


MD_SoD = MidiFile('Megadeth - Symphony of Destruction.mid')
JP_BtL = MidiFile('Judas Priest - Breaking the Law.mid')
JP_Pk  = MidiFile('Judas Priest - Painkiller (2).mid')
Me_MoP = MidiFile('Metallica - Master Of Puppets.mid')
Nw_OtHaFA = MidiFile('Nightwish - Over The Hills And Far Away.mid')

plt.subplot(4,1,1)
plot_tracks_note_quantity(MD_SoD.tracks[1:4],
                          ['Rhythm Guitar', 'Lead Guitar', 'Bass'],
                          'Megadeth - Symphony of Destruction')
plt.subplot(4,1,2)
plot_tracks_note_quantity(JP_BtL.tracks[1:4],
                          ['Rhythm Guitar', 'Lead Guitar', 'Bass'],
                          'Judas Priest - Breaking the Law')
plt.subplot(4,1,3)
plot_tracks_note_quantity(Me_MoP.tracks[1:6],
                          ['Hetfield', 'Hetfield(clean)', 'Hammet', 'Strings', 'Burton'],
                          'Metallica - Master Of Puppets')
plt.subplot(4,1,4)
plot_tracks_note_quantity(Nw_OtHaFA.tracks[1:8],
                          ['Strings', 'Synth Strings', 'Synth', 'Vocals', 'Bass', 'Solo Guitar', 'Rhythm Guitar'],
                          'Nightwish - Over The Hills And Far Away')

plt.savefig('Test.png')


# In[ ]:


#n_counter = Counter()
#for notes in Track_note_list:
#      n_counter += Counter(notes)


# In[ ]:


for i, track in enumerate(Nw_OtHaFA.tracks):
    print('Track {}: {}'.format(i, track))
print(Nw_OtHaFA.tracks)
    


# In[37]:





# TO-DO:
# 
#  - Analizar la duración de las notas.
