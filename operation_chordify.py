from music21 import *

def chordify_rn(s):
    s_chords = s.chordify(addTies=False,removeRedundantPitches=True) #IS WORKING     #chordify slices as every movement/diff chord
    key = s_chords.analyze('key')   #music21 function - tells us key signature
    chord_pair_dict = {}
    last_chord = 'nothing yet...'
    chord_pair_into_dictionary_tally = 0
    if key.mode == 'minor':
        print('KEY IS MINOR')
        key = key.relative
    print(key)
    for this_chord in s_chords.recurse().getElementsByClass('Chord'): #for every chord in the SONG....
        this_rn = roman.romanNumeralFromChord(this_chord, key)  #roman numeral of chord... has properties 'scaleDegree' and 'figure'
        this_chord.semiClosedPosition(forceOctave=4, inPlace=True)     #closedPosition means all the notes of the original chord are quished in the same octave so its easier to analyse
        this_chord.addLyric(str(this_rn.figure))

        #+++++  CREATING CHORD PAIR DICTIONARY     +++++++++++
        if last_chord != 'nothing yet...': #last chord can't exist if we're on the first chord of the sequence
            #create roman numeral version
            last_rn = roman.romanNumeralFromChord(last_chord, key)
            if last_rn.scaleDegree != this_rn.scaleDegree: #IF this chord is not the same as last chord
                #+++++++ ADD CHORDPAIR TO DICT    (in roman num form)
                chord_pair_name = ("{} -> {}".format(last_rn.figure, this_rn.figure))
                if chord_pair_name in chord_pair_dict: #if the chord pair has already occured
                    chord_pair_dict[chord_pair_name] += 1  #increase its tally by one
                else: #else (if this is the first time the chord pair has appeared)
                    chord_pair_dict[chord_pair_name] = 1 #enter it in the dictionary with a value of 1 (since it has occured once so far)

                #print("{} -> {}".format(last_rn.scaleDegree, this_rn.scaleDegree))
                chord_pair_into_dictionary_tally = chord_pair_into_dictionary_tally + 1
                if chord_pair_into_dictionary_tally > 100: #if 100 chord pairs have been observed from here
                    print('Abort')
                    break
                print(chord_pair_dict)
                print(chord_pair_into_dictionary_tally)
        last_chord = this_chord #this line has to always be last

    return chord_pair_dict
def get_key_sigs(s):
    s_chords = s.chordify(addTies=False,removeRedundantPitches=True)
    key = s_chords.analyze('key')
    return key
