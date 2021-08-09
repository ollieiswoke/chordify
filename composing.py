import statistics
import numpy
from music21 import *

def get_chord_options(chord_pair_dict, current_chord_num):         #
    "chord_options is a list of chords that have historically followed the current chord"
    chord_options = []
    chord_opts_dict = {} #dictionary of all chords that have historically followed the current chord
#for every pair of chords, if the first chord is current_chord_num, then add to list chord_options:
    for chord_pair in chord_pair_dict:
        if chord_pair.startswith(current_chord_num + " ->"):
            #print(current_chord_num + " ->")
            chord_opts_dict[chord_pair] = chord_pair_dict[chord_pair]
    for chord_num in chord_opts_dict:
        chord_num = chord_num.split(" -> ") #make a dictionary of chord_options that maps chord name to frequency
        chord_options.append(chord_num[1])
    print(chord_options)
    return chord_options

def get_corresponding_chord_probability(chord_pair_dict, current_chord_num): #chord options are chords that have historically followed the current chord
    """gets probability (as decimal) of each chord option.
    returns a list of decimals, in the same order as chord_opts"""
    corresponding_chord_probability = []
    total = 0
    chord_opts_dict = {} #dictionary of all chords that have historically followed the current chord
#this for loop gets the total options available (as int):
    for chord_pair in chord_pair_dict:
        if chord_pair.startswith(str(current_chord_num) + " ->"):
            chord_opts_dict[chord_pair] = chord_pair_dict[chord_pair]
            total += chord_opts_dict[chord_pair]
#for each option that COULD follow, append the chance of it following (individual freq/total freq):
    for chord_num in chord_opts_dict:
        chance = chord_opts_dict[chord_num]/total
        corresponding_chord_probability.append(chance)
    return corresponding_chord_probability

def markov_chain(chord_pair_dict, chord_prog, current_chord_num, choices_required):
    for next_chord in range(choices_required):
        chord_options = get_chord_options(chord_pair_dict, current_chord_num)
        corresponding_chord_probability = get_corresponding_chord_probability(chord_pair_dict, current_chord_num)
        last_chord = current_chord_num
        repeat_tally = 0 #how many times the while loop repeats. if this number gets higher than 2, the chords are stuck in a dead end (will repeat constantly like "I","V","I",V) In this case a new random chord should be chosen
        #print(current_chord_num)
        #print(chord_options)
        #print(corresponding_chord_probability)
        #these next four lines are just for the selection of the first chord, then a while loop is used
        if chord_options == []: #if there historically has been NO chord that follwed this... play the tonic instead:
            current_chord_num = 'I' #choose the tonic
        elif len(chord_options) > 1:
            current_chord_num = numpy.random.choice(chord_options, 1, p=corresponding_chord_probability)[0] #selects a chord, with percentage chance from corresponding chord probability

        if next_chord > 1: #if this is the second chord or later..
            while True: #this while loop ensures the current choice is not equal to the one 2 choices ago (aka avioding something like 6 3 6 3)
                repeat_tally +=1
                print(repeat_tally)
                if chord_options == []: #if there historically has been NO chord that follwed this... play a random chord
                    print("reached dead end... choosing tonic")
                    current_chord_num = 'I' #choose the tonic
                    break
                if repeat_tally > 5: #if the only options are ones that are forbidden (because they were played recently, and we don't want it to repeat)
                    print("got stuck in a loop, choosing a new starting point..")
                    current_chord_num = 'I'
                    break
                if current_chord_num == chord_prog[-2]: #if current chord = chord two times ago, try again
                    #print("     last chord was...", str(chord_prog[-2]))
                    continue
                if next_chord > 2:
                    if current_chord_num ==  chord_prog[-1]: #if current chord =last chord, try again
                        continue


                current_chord_num = numpy.random.choice(chord_options, 1, p=corresponding_chord_probability)[0]
                #print("chord choice is...", str(current_chord_num))
                break
        print("current chord is {}, chord options: {}".format(last_chord, chord_options))
        chord_prog.append(current_chord_num)
    return chord_prog

def choose_theme_a(chord_pair_dict):
    """This function returns a list of four chords as roman numerals (ie [1,5,6,4])
    using a markov chain and the data from the pieces"""
    theme_a = []
    first_chord = statistics.get_most_common_chords(chord_pair_dict)[:1] #first chord is the most common chord in the dictionary
    theme_a.append(first_chord)
    current_chord_num = first_chord
    markov_chain(chord_pair_dict, theme_a, current_chord_num, 3)
    return theme_a

def choose_random_chord(chord_pair_dict):
    """returns a str (ie "ii" or ""iv or "III"). The chord is chosen by
    (number of occurences of that choice)/(total occurences of every choice)"""
    chord_prog = []
    first_chord = statistics
    #getting list of ALL chords and storing in "chord_options"
    chord_options = []
    for chord_pair in chord_pair_dict:
        chord_pair = chord_pair.split(" -> ")
        print(chord_pair, chord_pair[0])
        chord_options.append(chord_pair[0])
    #getting "corresponding_chord_probability"
    corresponding_chord_probability = []
    total = 0
    for chord_pair in chord_pair_dict:
        total += chord_pair_dict[chord_pair] #this loop gets total number of chords in song

    for chord_num in chord_pair_dict:
        chance = chord_pair_dict[chord_num]/total #for every chord in the dictionary, find chance of occurence and add to "corresponding_chord_probability"
        corresponding_chord_probability.append(chance) #for each option that COULD follow, append the chance of it following
    print("chord options", chord_options)
    print("corresponging chord probability", corresponding_chord_probability)
    chosen_chord = numpy.random.choice(chord_options, 1, p=corresponding_chord_probability)[0]
    return(chosen_chord)

def get_stream_from_chord_prog(chord_prog, key):
    """returns a music 21 stream from the chord progression
    chord_prog is currently in figured scale degrees (I, ii24, etc)
    """
    #print(chord_prog)
    stream_chord_prog = stream.Stream()
    quintet = get_voice_led_quintet(chord_prog, key) #gets tuple of eight notes for bassline (except not lowered an octave). its actually a quintet with five parts. We only want 2 of the parts
    counter = 0
    for scale_figure in chord_prog:
        comp_chord = roman.RomanNumeral(scale_figure, key) # this creates a music21 object from the scale degree
        chord_pitches_list = list(comp_chord.pitches)    #We want to add bass note to chord object, however, chord object is tuple and tuple can't be manipulated (tuples are immutable)
        #bass_note = comp_chord.bass() #gets lowest note from 'chord'
        bass_note = note.Note(quintet[0][counter])
        bass_note.octave = bass_note.octave - 2  #<<<#lowers the octave by TWO, making the note lower
        chord_pitches_list.append(bass_note)        #<<made list of tuple and added bass note to it

        high_note = note.Note(quintet[3][counter])
        high_note.octave = high_note.octave + 1  #<<<#raises the octave by ONE, making the note higher
        chord_pitches_list.append(high_note)        #<<chord pitches list is the list that is about to be added the strea,

        chord_pitches_tuple = tuple(chord_pitches_list)     #turn edited version  of chord into a tuple
        comp_chord = chord.Chord(chord_pitches_tuple)    #make chord object out of tuple
        comp_chord.duration.quarterLength = 4.0     #this turns the chord into actual notes with a duration so it can be added onto the music21 stream
        stream_chord_prog.append(comp_chord)
        counter += 1

    return stream_chord_prog

def get_voice_led_quintet(chord_prog, key):
    "makes a list of all possible voicings (configurations) of the bass"
    "iterates through each voicing and returns the one with smallest intervals"
    "there are three ways to represent each chord, so the number of possibilties are 3^n where n is number of chords. (in this case n=8)"
    #make list of lists of every possible chord combination
    music21_chord_prog = [] #chords of music 21object
    all_voicings = [] #this is a very large list of lists. each smaller list contains 4 notes (music21 objects.) this is every POSSIBLE way to write the bassline
    current_voicing = [] #is appended to "all_voicings" every iteration of the for loop below
    for scale_figure in chord_prog:
        music21_chord_prog.append(roman.RomanNumeral(scale_figure, key))
    for chord_note_1 in music21_chord_prog[0].pitches: #for every note in the first chord
        for chord_note_2 in music21_chord_prog[1].pitches: #go through every option for second chord
            for chord_note_3 in music21_chord_prog[2].pitches: #etc...
                for chord_note_4 in music21_chord_prog[3].pitches:
                    for chord_note_5 in music21_chord_prog[4].pitches:
                        for chord_note_6 in music21_chord_prog[5].pitches:
                            for chord_note_7 in music21_chord_prog[6].pitches:
                                for chord_note_8 in music21_chord_prog[7].pitches:
                                    current_voicing = [chord_note_1, chord_note_2, chord_note_3,chord_note_4, chord_note_5, chord_note_6, chord_note_7, chord_note_8]
                                    #print(current_voicing)
                                    #print(len(current_voicing))
                                    all_voicings.append(current_voicing) #add this possiblity to all voicings
                                    current_voicing = [] #reset current voicing for next iteration
    dict_voicing_intervals = {} #Maps a voicing (tuple of note objects) to the sum of all its intervals (into). sum of intervals shows us how jumpy or smooth the part is
    for current_voicing in all_voicings: #for EVERY POSSIBLE voicing of the chords
        "convert voicing to contain note objects, instead of pitch objects:"
        note_obj_voicings = [] #current_voicings are pitch objects, but need to be converted to note objects to be taken into "NNoteLinear NNoteLinearSegment" below
        for pitch_obj in current_voicing:
            note_obj_voicings.append(str(pitch_obj.nameWithOctave)) #creates note object from pitch (includes octave for better voice leading)

        LinSeg = voiceLeading.NNoteLinearSegment(note_obj_voicings) # a special object that allows for intervals to be checked in between, pitches needed to be converted into  notes

        "determine smoothness of voicing and adds to dictionary. dict_voicing_intervals has voicing as key and interval sum as value"
        "requires LinSeg, note_obj_voicings, dict_voicing_intervals"
        sum_of_intervals = 0
        for word_interval in LinSeg.melodicIntervals: #worded interval is 'm3', etc, but we want number of semitones to add up more accurately
            sum_of_intervals += abs(word_interval.semitones) #.semtitones results the interval as an int so its calculatable
            dict_voicing_intervals[tuple(note_obj_voicings)] = sum_of_intervals

        "Finds smoothest voicings and adds them to a list, then randomly selects one"
        import operator
        sorted_dict_voicing_intervals = sorted(dict_voicing_intervals.items(), key=operator.itemgetter(1)) #sorted dictionary is ordered from smoothest to least

        #print(note_obj_voicings, LinSeg.noteList)
    #print(sorted_dict_voicing_intervals[0], sorted_dict_voicing_intervals[1],sorted_dict_voicing_intervals[2])
    #print(sorted_dict_voicing_intervals[0][0])
    print(len(all_voicings)) #quintet currently doubles up too much. so for now only 2 quintet notes are used
    quintet = [sorted_dict_voicing_intervals[1][0], #dictionary is ordered. so [1] is the SMOOTHEST
    sorted_dict_voicing_intervals[2][0],
    sorted_dict_voicing_intervals[3][0],
    sorted_dict_voicing_intervals[4][0],
    sorted_dict_voicing_intervals[10][0]]
    #for part in quintet:
    #    print(part)
    return quintet

def choose_theme_b(chord_pair_dict):
    """This funct returns a LIST of ints representing the chords in a theme B
    The theme chooses a first chord giving any option
    (number of occurences of that choice)/(total occurences of every choice)
    And then uses markov chain. this selection is a group of 8 (not a group of 4),
    to create variation"""
    chord_prog = []
    first_chord = choose_random_chord(chord_pair_dict)
    chord_prog.append(first_chord)
    current_chord_num = first_chord
    print(current_chord_num)
    markov_chain(chord_pair_dict, chord_prog, current_chord_num, 7) #adds seven more chords to chord prog..
    return chord_prog

def get_voice_led_stream(stream_full_song, quintet, counter, chord_pitches_list):
    "add each of the five parts to chord_pitches_list ... which is the chord that gets added"

    for quintet_note_obj_list in quintet: #for each of the five parts
        comp_note_obj = note.Note(quintet_note_obj_list[counter])
        #comp_note_obj.octave = comp_note_obj.octave - 1 #comp_note_obj is note about to be added to chord
        chord_pitches_list.append(comp_note_obj) #add their current note to comp_chord
    return stream_full_song

def composing(chord_pair_dict):
    """This function would or could be called in main to create a full song,
    however only theme B is necessary, and adding more would increase the
    loading time"""
    full_song = []
    full_song.append(choose_theme_a(chord_pair_dict))
    full_song.append(choose_theme_b(chord_pair_dict))
    full_song.append(choose_theme_a(chord_pair_dict))
    stream_full_song = get_stream_from_chord_prog(full_song)
    stream_full_song = get_voice_led_stream(stream_full_song) #stub
    return
