
def get_most_common_chords(chord_pair_dict):
    "Finds the chord that occured the most times in the piece"
    "Returns a chord name as a string (eg iv6)"
    max_occurance = 0 #max occurance
    for chord_pair in chord_pair_dict:
        if chord_pair_dict[chord_pair] > max_occurance:
            max_occurance = chord_pair_dict[chord_pair] #new maximum = current chord
            max_chord_pair_name = chord_pair
    most_common_chord = max_chord_pair_name
    return most_common_chord
def get_most_common_chord_after_tonic(chord_pair_dict):
    chord_opts_after_tonic = {} #dictionary of all desired chord type
    #fills chord_opts_after_tonic with every option that starts with the tonic from chord_pair_dict
    for chord_pair in chord_pair_dict:
        if chord_pair.startswith("I ->"):
            chord_opts_after_tonic[chord_pair] = chord_pair_dict[chord_pair]
    return get_most_common_chords(chord_opts_after_tonic)

def get_most_common_chord_ending_on_tonic(chord_pair_dict):
    #very similar to above function but is instead looking for chord pairs in chord_pair_dict that ENDED on tonic
    chord_opts_ending_on_tonic = {} #dictionary of all desired chord type
    for chord_pair in chord_pair_dict:
        if chord_pair.endswith("-> I"):
            chord_opts_ending_on_tonic[chord_pair] = chord_pair_dict[chord_pair]
    return get_most_common_chords(chord_opts_ending_on_tonic)
def present_stat_report(chord_pair_dict,key, chord_prog):
    statistics_report = ["key signature: {}".format(key),
    "{} was the MOST common chord progression!".format(get_most_common_chords(chord_pair_dict)),
    "{} was the most common chord progression that started on the tonic".format(get_most_common_chord_after_tonic(chord_pair_dict)),
    "{} was the most common chord pair that ended on the tonic".format(get_most_common_chord_ending_on_tonic(chord_pair_dict)),
    "{} was ChordBot's progression, based on the piece provided".format(chord_prog)]
    return statistics_report
