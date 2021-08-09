from music21 import converter
from music21 import *
import operation_chordify
import statistics
from composing import *

def chordbot(song_file_name, mode):
    song_file_path = r'midi/{}.mid'.format(song_file_name)
    s = converter.parse(song_file_path)   #s is the raw music21 "stream" object from the selected midi file
    key = operation_chordify.get_key_sigs(s)
    if mode == "real": #real data set is used and analysed
        chord_pair_dict = operation_chordify.chordify_rn(s)
        #print(statistics.present_stat_report(chord_pair_dict, key))
    if mode == "test": #test data set is used in this option, so loading time is reduced
        chord_pair_dict = {'v5 -> I64': 2, 'I76 -> ii4': 2, 'iv52 -> v62': 2, 'ii4 -> vi': 2, 'iii5 -> I65': 2,
        'I64 -> iii5': 2, 'ii2 -> i': 3, 'I72 -> v5':2,'iv7 -> ii6': 2, 'ii7 -> v4': 2, 'viio64 -> iv5': 2,
        'v+4 -> #iib8': 2, 'vi -> V': 2, 'iv5 -> viio64': 2, 'v2 -> iv52': 2, '#iib7 -> v+4': 2, 'iv -> I': 2,
        'iii -> #iib7': 2, 'i4 -> v5': 2, 'vi4 -> v+4': 2, 'i74 -> ii5': 2, 'I6b5 -> vi64': 2, 'V -> i': 2,
        'v5 -> i4': 2, 'i -> v2': 1, 'ii -> i5': 2, 'v62 -> iv7': 2, 'iii7 -> I76': 4, 'ii7 -> iv': 3, 'I76 -> iii7': 2,
        'I -> ii2': 2, 'i -> ii2': 2, 'iv5 -> iii7': 2, 'iv5 -> ii6': 2, 'v4 -> I72': 2, 'ii6 -> iv5': 2, 'v4 -> ii': 2,
        'i5 -> iii7': 2, 'v+4 -> i74': 4, 'ii6 -> iv': 2, 'i74 -> v+4': 2, 'ii7 -> i5': 1, 'iii -> vi4': 2, 'vi64 -> v+4': 2,
        'I65 -> iii7': 2, 'iii7 -> I65': 2, 'i -> iii': 2,'i -> II#3': 2, '#iv -> v2': 1}
        if key.mode == 'minor':
            print('KEY IS MINOR')
            key = key.relative   #if key is minor, Chordbot still wants to analyse it as if its the major counterpart. Therefore, convert key to key.relative (relative major key signature)

    print(chord_pair_dict)
    chord_prog = choose_theme_b(chord_pair_dict) #chord_prog is a list [], with strings describing each chord
    print(chord_prog)
    #get_voice_led_bass(chord_prog, key)
    stream_full_song = get_stream_from_chord_prog(chord_prog,key) #gets music21 stream object from chord progression
    print("stream is made")
    #stream_full_song = get_voice_led_stream_on_many_instruments(stream_full_song)
    #stream_full_song.show("midi")
    output_path = r'output/{}_inspired_piece.mid'.format(song_file_name)
    fp = stream_full_song.write('midi', fp=output_path) #writes midi file out to desired location (user downloads it later)
    print(statistics.present_stat_report(chord_pair_dict, key, chord_prog))
    return statistics.present_stat_report(chord_pair_dict, key, chord_prog)
    
