# Copyright (c) 2010-2013, Regents of the University of California.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  - Neither the name of the Regents of the University of California nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import sys
import os

import pathHelper
if __name__=="__main__":
    pathHelper.updatePath()

import logging
log = logging.getLogger('openVisualizerCli')

from   cmd         import Cmd

from moteState     import moteState
import openVisualizerApp
import openvisualizer_utils as u


class OpenVisualizerCli(Cmd):
        
    def __init__(self,app):
        log.info('Creating OpenVisualizerCli')
        
        # store params
        self.app                    = app
        
        Cmd.__init__(self)
        self.doc_header = 'Commands (type "help all" or "help <topic>"):'
        self.prompt     = '> '
        self.intro      = '\nOpenVisualizer  (type "help" for commands)'
        
    #======================== public ==========================================
    
    #======================== private =========================================
    
    #===== callbacks
    
    def do_state(self, arg):
        """
        Prints provided state, or lists states.
        Usage: state [state-name]
        """
        if not arg:
            for ms in self.app.moteStates:
                output  = []
                output += ['Available states:']
                output += [' - {0}'.format(s) for s in ms.getStateElemNames()]
                self.stdout.write('\n'.join(output))
            self.stdout.write('\n')
        else:
            for ms in self.app.moteStates:
                try:
                    self.stdout.write(str(ms.getStateElem(arg)))
                    self.stdout.write('\n')
                except ValueError as err:
                    self.stdout.write(err)
    
    def do_list(self, arg):
        """List available states. (Obsolete; use 'state' without parameters.)"""
        self.do_state('')
    
    def do_root(self, arg):
        """
        Sets dagroot to the provided mote, or lists motes
        Usage: root [serial-port]
        """
        if not arg:
            self.stdout.write('Available ports:')
            if self.app.moteStates:
                for ms in self.app.moteStates:
                    self.stdout.write('  {0}'.format(ms.moteConnector.serialport))
            else:
                self.stdout.write('  <none>')
            self.stdout.write('\n')
        else:
            for ms in self.app.moteStates:
                try:
                    if (ms.moteConnector.serialport==arg):
                        ms.triggerAction(moteState.moteState.TRIGGER_DAGROOT)
                except ValueError as err:
                    self.stdout.write(err)
                
    def help_all(self):
        """Lists first line of help for all documented commands"""
        names = self.get_names()
        names.sort()
        maxlen = 65
        self.stdout.write(
            'type "help <topic>" for topic details\n'.format(80-maxlen-3))
        for name in names:
            if name[:3] == 'do_':
                try:
                    doc = getattr(self, name).__doc__
                    if doc:
                        # Handle multi-line doc comments and format for length.
                        doclines = doc.splitlines()
                        doc      = doclines[0]
                        if len(doc) == 0 and len(doclines) > 0:
                            doc = doclines[1].strip()
                        if len(doc) > maxlen:
                            doc = doc[:maxlen] + '...'
                        self.stdout.write('{0} - {1}\n'.format(
                                                name[3:80-maxlen], doc))
                except AttributeError:
                    pass
    
    def do_quit(self, arg):
        self.app.close()
        return True


#============================ main ============================================

if __name__=="__main__":
    app = openVisualizerApp.main()
    cli = OpenVisualizerCli(app)
    cli.cmdloop()
