__author__ = 'arjun_prasad_namdeo'

import os
import re

import config as mod_cfg
import scripts.common.general as mod_general
import scripts.common.validate as mod_validate


def setCommand_In():
    '''
    this will query the DJV binary file and set init command for the same
    for Ubuntu, DJV Static binary not working.. Need to install it from http://djv.sourceforge.net/
    '''

    library_bin_file = "djv_convert"
    if mod_cfg.os_family == "Windows":
        library_bin_file = os.path.join(mod_cfg.packagePath, "bin", mod_cfg.os_family, "djv/bin/djv_convert.exe")

    return library_bin_file

def execute_Process(processType=None, arguments=None):
    '''
    this process will pass the user inputs and create an object and execute process
    '''
    obj = ImgConvert(arguments)
    obj.process(processType)

    print "\n You Rocks Dude...!!! Process completed...!!!"


class ImgConvert(object):
    '''
    This class having attributes and methods related to DJV Process
    '''

    def __init__(self, args=None):
        self.arguments = args
        self.cmd_exe = setCommand_In()

    def set_inputPath(self):
        self.cmd_input = mod_validate.Validation.isValid_Sequence(self.arguments.inputPath)
        if not self.cmd_input:
            if mod_validate.Validation.isValid_SingleFile(self.arguments.inputPath):
                self.cmd_input = self.arguments.inputPath

        self.cmd_input = mod_general.get_seq_name_from_filePath(self.cmd_input, "djv")

    def set_outputPath(self):
        frmPadding = mod_general.get_seq_padding_count_from_outputString(self.arguments.outputPath)
        print ">>> frmPadding : ", frmPadding
        if frmPadding:
            if "#" in self.arguments.outputPath:
                seq_pad = re.search("#+", self.arguments.outputPath).group(0)
            else:
                seq_pad = re.search("%\d+d", self.arguments.outputPath).group(0)
            self.cmd_output = str(self.arguments.outputPath).replace(seq_pad, str(1).zfill(int(frmPadding)))
        else:
            self.cmd_output = str(self.arguments.outputPath)

    def set_outputRes(self):
        self.cmd_res = ""
        if self.arguments.resolution:
            self.cmd_res = "-resize %s %s " % (self.arguments.width, self.arguments.height)
        else:
            if self.arguments.width:
                self.cmd_res = "-width %s " % (self.arguments.width)

            if self.arguments.height:
                self.cmd_res = "-height %s " % (self.arguments.height)

    def set_quality(self, imageExt=".dpx"):
        '''
        Please refer to http://djv.sourceforge.net/djvImageIo.html for more options
        '''
        self.cmd_quality = ""
        quality = {".dpx" : "",
                   ".jpg" : "-jpeg_quality 100",
                   ".jpeg" : "-jpeg_quality 100"}

        if imageExt in quality.keys():
            self.cmd_quality += quality.get(imageExt)


    def process(self, processType=None):
        self.set_inputPath()
        self.set_outputPath()
        self.set_outputRes()
        self.set_quality()

        #print self.cmd_exe, self.cmd_input, self.cmd_output, self.cmd_res, self.cmd_quality

        command = " ".join([self.cmd_exe, self.cmd_input, self.cmd_output, self.cmd_res, self.cmd_quality])
        #print command
        mod_general.run_in_terminal(command)



