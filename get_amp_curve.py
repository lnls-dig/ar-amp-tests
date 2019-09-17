import argparse
import csv
from epics import caget,caput
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('output', type=str, help='Output file')
parser.add_argument('-s', '--spectrum', type=str, default='DIG:RSFSV:', help='Spectrum analyzer PV prefix')
parser.add_argument('-r', '--rf_gen', type=str, default='DIG:RSSMB100A:', help='RF Generator PV prefix')
parser.add_argument('-f', '--freq', type=int, default=200000000, help='RF Frequency used for the test')
parser.add_argument('-a', '--amp', type=str, default='DIG:ARAMP250:', help='RF Amplifier PV prefix')
parser.add_argument('-t', '--step', type=int, default=8, help='Gain step size')
parser.add_argument('--sleep', type=float, default=0.5, help='Sleep time between steps')
args = parser.parse_args()

rfgen_output_enable_pv = args.rf_gen+'GeneralRF-Sel'
rfgen_freq_pv = args.rf_gen+'GeneralFreq-SP'
rfgen_output_level_pv = args.rf_gen+'GeneralRFLvl-SP'

amp_gain_step_pv = args.amp+'GainStep-SP'
amp_output_enable_pv = args.amp+'Enbl-Sel'

fsl_mark1_en_pv = args.spectrum+'EnblMark1-Sel'
fsl_mark1_max_auto_pv = args.spectrum+'EnblMaxAuto1-Sel'

fsl_center_freq_pv = args.spectrum+'FreqCenter-SP'
fsl_freq_span_pv = args.spectrum+'FreqSpan-SP'
fsl_ref_lvl_pv = args.spectrum+'RefLvl-SP'

fsl_mark1_y_pv = args.spectrum+'MarkY1-Mon'
fsl_get_spectrum_pv = args.spectrum+'GetSpectrum-Sel'

#Configure RF Generator
caput(rfgen_output_enable_pv, 0)
caput(rfgen_freq_pv, args.freq)
caput(rfgen_output_level_pv, -20)

#Configure RF Amplifier
caput(amp_gain_step_pv, 0)
caput(amp_output_enable_pv, 0)

#Configure Spectrum Analyzer
caput(fsl_mark1_en_pv, 1)
caput(fsl_mark1_max_auto_pv, 1)
caput(fsl_center_freq_pv, args.freq)
caput(fsl_freq_span_pv, (args.freq/2))
caput(fsl_ref_lvl_pv, 0)
caput(fsl_get_spectrum_pv, 1)
 
raw_input('Equipments configured, press Enter to start test!')

#Enable RF
caput(rfgen_output_enable_pv, 1)
caput(amp_output_enable_pv, 1)

#Sweep gain steps
power_output = []

for step in range(0, 4096, args.step):
    sleep(args.sleep)
    caput(amp_gain_step_pv, step)
    output = caget(fsl_mark1_y_pv)
    power_output.append([step,output])
    print('STEP: '+str(step)+'\tOUTPUT: '+str(output))

#Disable amp
caput(amp_gain_step_pv, 0)
caput(amp_output_enable_pv, 0)

#Disable RF Generator
caput(rfgen_output_enable_pv, 0)

#Write output file
with open(args.output, 'w') as out_file:
    writer = csv.writer(out_file)
    writer.writerows(power_output)
