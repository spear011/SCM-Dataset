NSYNTH_SAMPLE_RATE = 16000
sr = 16000
NSYNTH_VELOCITIES = [25, 50, 75, 100, 127]
release_in_sample = int(100 * 0.001 * sr)
attack_in_sample = int(5 * 0.001 * sr)


INST_FAM_LIST = ["keyboard", "organ", "synth_lead",  "mallet",  "guitar", "bass",  "string", "flute", "vocal", "brass", "reed",  "etc", "drum"]
INST_FAM_dict = {INST_FAM_Values : INST_FAM_Keys for INST_FAM_Keys, INST_FAM_Values in zip(INST_FAM_LIST, range(len(INST_FAM_LIST)))}

INST_MAP = {
    'accordion' : 1, 
    'acoustic_bass' : 5, 
    'acoustic_guitar' : 4, 
    'acoustic_piano' : 0,
    'bassoon': 9, 
    'bell' : 3, 
    'brass_ensemble' : 9, 
    'celesta' : 0, 
    'choir' : 8,
    'clarinet' : 7, 
    'electric_bass' : 5, 
    'electric_guitar_clean' : 4,
    'electric_guitar_distortion' : 4, 
    'electric_piano' : 0, 
    'flute' : 7,
    'glockenspiel' : 3, 
    'harp' : 6, 
    'horn' : 9, 
    'marimba' : 3, 
    'nylon_guitar' : 4, 
    'oboe' : 7,
    'orgel' : 1, 
    'string_cello' : 6, 
    'string_double_bass' : 5, 
    'string_ensemble' : 6,
    'string_viola' : 6, 
    'string_violin' : 6, 
    'synth_bass' : 5, 
    'synth_bass_wobble' : 5,
    'synth_bell' : 3, 
    'synth_pad' : 2, 
    'synth_pluck' : 2, 
    'synth_voice' : 8, 
    'timpani' : 3,
    'trombone' : 9, 
    'tuba' : 9, 
    'vibraphone' : 3, 
    'xylophone' : 3
}