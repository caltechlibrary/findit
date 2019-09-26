import os
import os.path as path
from   threading import Thread

from   pubsub import pub
import wx


from .exceptions import *
from .files import readable, writable, file_in_use
from .network import network_available


class MainBody(Thread):
    '''Main body of Check It! implemented as a Python thread.'''

    def __init__(self, infile, outfile, controller, accessor, notifier, tracer, debug):
        '''Initializes main thread object but does not start the thread.'''
        Thread.__init__(self, name = "MainBody")

        # Make this a daemon thread, but only when using the GUI; for CLI, it
        # must not be a daemon thread or else the program exits immediately.
        if controller.is_gui:
            self.daemon = True

        # We expose one attribute, "exception", that callers can use to find
        # out if the thread finished normally or with an exception.
        self.exception = None

        # The rest of this sets internal variables.
        self._infile     = infile
        self._outfile    = outfile
        self._debug      = debug
        self._controller = controller
        self._tracer     = tracer
        self._accessor   = accessor
        self._notifier   = notifier
        self._interrupted = False


    def run(self):
        # Set shortcut variables for better code readability below.
        infile     = self._infile
        outfile    = self._outfile
        debug      = self._debug
        controller = self._controller
        accessor   = self._accessor
        notifier   = self._notifier
        tracer     = self._tracer

        # Preliminary sanity checks -------------------------------------------

        tracer.start('Performing initial checks')
        if not network_available():
            notifier.fatal('No network connection.')
            return

        if not infile and controller.is_gui:
            tracer.update('Asking user for input file')
            infile = controller.open_file('Open barcode file', 'CSV file|*.csv|Any file|*.*')
        if not infile:
            tracer.update('No input file -- nothing to do')
            return
        if not readable(infile):
            tracer.update('Cannot read file: {}'.format(infile))
            return

        if not outfile and controller.is_gui:
            tracer.update('Asking user for output file')
            outfile = controller.save_file('Output destination file')
        if not outfile:
            tracer.update('No output file specified -- cannot continue')
            return
        if path.exists(outfile):
            if file_in_use(outfile):
                tracer.update('File is open by another application: {}'.format(outfile))
                return
            elif not writable(outfile):
                tracer.update('Unable to write to file: {}'.format(outfile))
                return
        else:
            dest_dir = path.dirname(outfile) or os.getcwd()
            if not writable(dest_dir):
                tracer.update('Cannot write to folder: {}'.format(dest_dir))
                return

        # Main work -----------------------------------------------------------



    def stop(self):
        pass
