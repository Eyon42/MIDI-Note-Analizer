#!/usr/bin/env python
# coding: utf-8
'''
This is a script for generating a csv file with a dict mapping midi note codes to the name of the notes
'''


import csv

def midi_note_dict_generator():
    note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    octave = 0
    curr_note = 0
    note_dict = {}
    for i in range(21,128):
        note_dict[i] = f'{note_names[curr_note] + str(octave)}'
        if curr_note == 2:
            octave += 1

        if curr_note == 11:
            curr_note = 0
        else:
            curr_note += 1
    
    return note_dict

midi_note_dict = midi_note_dict_generator()

with open('Midi_notes.csv', mode='w') as file:
    fieldnames = midi_note_dict.keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(midi_note_dict)


#Code to read the file
with open('Midi_notes.csv') as di:
    read = csv.DictReader(di)
    midi_note_dict_2 = next(read)
    
print(midi_note_dict_2)

