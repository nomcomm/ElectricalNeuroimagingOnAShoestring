"""
Independent Study 
=============

Positive versus Neutral stimulus presentation.

"""

from time import time
from optparse import OptionParser
from glob import glob
from random import choice

import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet


def present(duration=120):

    # Create markers stream outlet
    info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
    outlet = StreamOutlet(info)

    markernames = [1, 2]
    start = time()

    # Set up trial parameters
    n_trials = 2010
    iti = 0.8
    soa = 0.2
    jitter = 0.2
    record_duration = np.float32(duration)

    # Setup trial list
    image_type = np.random.binomial(1, 0.5, n_trials)
    trials = DataFrame(dict(image_type=image_type,
                            timestamp=np.zeros(n_trials)))

    # Setup graphics

    def load_image(filename):
        return visual.ImageStim(win=mywin, image=filename)

    mywin = visual.Window([1600, 900], monitor='testMonitor', units='deg', winType='pygame',
                          fullscr=True)
    positives = list(map(load_image, glob(
        'stimulus_presentation/stim/Positive_neutral/Positive/*.bmp')))
    neutrals = list(map(load_image, glob(
        'stimulus_presentation/stim/Positive_neutral/Neutral/*.bmp')))

    for ii, trial in trials.iterrows():
        # Intertrial interval
        core.wait(iti + np.random.rand() * jitter)

        # Select and display image
        label = trials['image_type'].iloc[ii]
        image = choice(positives if label == 1 else neutrals)
        image.draw()

        # Send marker
        timestamp = time()
        outlet.push_sample([markernames[label]], timestamp)
        mywin.flip()

        # offset
        core.wait(soa)
        mywin.flip()
        if len(event.getKeys()) > 0 or (time() - start) > record_duration:
            break
        event.clearEvents()

    # Cleanup
    mywin.close()


def main():
    parser = OptionParser()

    parser.add_option("-d", "--duration",
                      dest="duration", type='int', default=120,
                      help="duration of the recording in seconds.")

    (options, args) = parser.parse_args()
    present(options.duration)


if __name__ == '__main__':
    main()
