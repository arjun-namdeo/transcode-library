__author__ = 'arjun_prasad_namdeo'

import os
import re

import config as mod_cfg
import scripts.common.general as mod_general
import scripts.common.validate as mod_validate

def setCommand_In():
    '''
    this will query the FFmpeg binary file and set init command for the same

    '''
    library_bin_file = os.path.join(mod_cfg.packagePath, "bin", mod_cfg.os_family, "ffmpeg/ffmpeg")
    if mod_cfg.os_family == "Windows":
        library_bin_file = os.path.join(mod_cfg.packagePath, "bin", mod_cfg.os_family, "ffmpeg/ffmpeg.exe")

    return library_bin_file

def execute_Process(processType=None, arguments=None):
    '''
    this process will pass the user inputs and create an object and execute process
    '''
    obj = Convert(arguments)
    obj.process(processType)

    print "\n You Rocks Dude...!!! Process completed...!!!"

class Convert(object):
    '''
    This class having attributes and methods related to FFMpeg Process
    '''
    def __init__(self, arguments=None):
        self.args = arguments
        self.cmd_exe = setCommand_In()
        #print self.cmd_exe

    def set_VideoCodec(self):
        if not self.args.videoCodec:
            self.cmd_vcodec = ""
            return

        self.cmd_vcodec = "-c:v %s  " % self.args.videoCodec

        vc_dict = {"libx264" : "-profile:v high444 -crf 5 -pix_fmt yuv420p ",
                   "prores" : "-profile:v 3 -pix_fmt yuv420p ",
                   "dnxhd" : "-b:v 185M -pix_fmt yuv422p -mbd rd -an ",
                   "mjpeg" : "-b:v 16M -qscale 2  -pix_fmt yuv420p -vcodec mjpeg -crf 2 "}

        if self.args.videoCodec in vc_dict.keys():
            self.cmd_vcodec += vc_dict.get(self.args.videoCodec)

    def set_Fps(self):
        self.cmd_fps = "-r %s" % self.args.frameRate

    def set_text_overlay(self):
        self.cmd_text = ""
        if not self.args.textData:
            return

        print self.args.textColor

        textColor = mod_general.rgb_to_hex(self.args.textColor)
        textOpac = float(self.args.textOpacity)/100
        textFont = "\\\\".join([mod_general.get_font_path()[1], self.args.textFontFamity])

        self.cmd_text = "drawtext=fontfile='{TF}.ttf': text='{TD}': x={X}: y={Y}: fontsize={TS}: fontcolor={TC}@{TO}".format(TF=textFont,
                                                    TD=self.args.textData, X=self.args.textPosition[0],
                                                    Y=self.args.textPosition[1], TS=self.args.textSize,
                                                    TC=textColor, TO=textOpac)

    def set_Threads(self):
        self.cmd_thread = "-threads 8"

    def set_inputPath(self, inputType=None):
        if "#" in self.args.inputPath:
            self.args.inputPath = mod_general.get_seq_name_from_filePath(self.args.inputPath, "ffmpeg")

        self.cmd_input = "-y -i %s" % self.args.inputPath

        if inputType:
            self.cmd_input = "-y -f %s -i %s" % (inputType, self.args.inputPath)

    def set_outputPath(self):
        if "#" in self.args.outputPath:
            hashPad = re.search("#+", self.args.outputPath).group(0)

            self.args.outputPath = self.args.outputPath.replace(hashPad, "%{0}d".format(str(len(hashPad)).zfill(2)))


        self.cmd_output = self.args.outputPath

    def set_filter(self):
        self.cmd_filter = ""
        self.set_text_overlay()

        if self.args.textData:
            self.cmd_filter = '-filter_complex "%s" ' % self.cmd_text

    def process(self, type):
        '''
        @:param type :  it's process type, it can be any of below
                        img2mov, img2img, mov2mov, mov2img
        '''

        if type == "img2mov":
            self.set_inputPath("image2")
        else:
            self.set_inputPath()

        self.set_VideoCodec()
        self.set_outputRes()
        self.set_filter()
        self.set_Fps()
        self.set_Threads()
        self.set_outputPath()

        command = " ".join([self.cmd_exe, self.cmd_input, self.cmd_res, self.cmd_filter, self.cmd_fps, self.cmd_thread, self.cmd_vcodec, self.cmd_output])
        #print "\n", command
        mod_general.run_in_terminal(command)

    def set_outputRes(self):
        self.cmd_res = ""
        if self.args.resolution:
            self.cmd_res = "-s %sx%s -aspect %s " % (self.args.width, self.args.height, self.args.aspectRatio)
        else:

            if self.args.width and self.args.height:
                aspectRatio = float(self.args.width)/float(self.args.height)
                self.cmd_res = "-s %sx%s -aspect %s " % (self.args.width, self.args.height, aspectRatio)
            else:
                if self.args.width:
                    self.cmd_res = "-vf scale=%s:-1" % (self.args.width)

                if self.args.height:
                    self.cmd_res = "-vf scale=-1:%s" % (self.args.height)

        if self.args.scale:
            percent = float(self.args.scale)/100.0
            self.cmd_res = "-vf scale=%s*iw:-1" % (percent)



