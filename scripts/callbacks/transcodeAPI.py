__author__ = 'arjun_prasad_namdeo'

import os
import re

import config as mod_cfg
import scripts.common.parser as mod_parser
import scripts.common.validate as mod_validate
import scripts.common.general as mod_general
import scripts.packages.mod_ffmpeg as mod_ffmpeg
import scripts.packages.mod_djv as mod_djv

for mod in [mod_parser, mod_cfg, mod_validate, mod_general, mod_ffmpeg, mod_djv]:
    reload(mod)

class Transcode(object):
    '''
    This is the main trascode class, You have to create a transcode object with the arguments.
    for detail arguments, check function main() in this module.

    Once you created the object from this class you can process, query as per requirement. those are the methods.

    '''
    def __init__(self, args=None):
        self.arguments = args

    def process(self):
        if not Transcode.validate(self.arguments):
            return

        processType, lib = self.get_process_type()
        if not processType:
            return


        if self.arguments.textData:
            mod_ffmpeg.execute_Process(processType, self.arguments)
        else:
            if processType == "img2img":
                if lib == "djv":
                    mod_djv.execute_Process(processType, self.arguments)
                else:
                    mod_ffmpeg.execute_Process(processType, self.arguments)
            else:
                mod_ffmpeg.execute_Process(processType, self.arguments)

    def get_process_type(self):
        '''
        self.get_process_type()  =  based on user input check the process types and which library to use

        processType can be [img2img, img2mov, mov2mov, mov2img]
        library can be [djv, ffmpeg, ocio, oiio]
        '''
        processType = None
        inputExt = mod_general.get_file_extension(self.arguments.inputPath)
        outputExt = mod_general.get_file_extension(self.arguments.outputPath)

        library = "djv"

        if inputExt in mod_cfg.valid_imgFileTypes:
            if inputExt in ['.dpx', 'exr']:
                library = "ffmpeg"

            if outputExt in mod_cfg.valid_movFileTypes:
                processType = "img2mov"
                if not self.arguments.videoCodec:
                    print ">>> Please provide a video codec from %s " % mod_cfg.valid_VideoCodec
                    return False

            if outputExt in mod_cfg.valid_imgFileTypes:
                processType = "img2img"

        if inputExt in mod_cfg.valid_movFileTypes:
            if outputExt in mod_cfg.valid_movFileTypes:
                processType = "mov2mov"
                if not self.arguments.videoCodec:
                    print ">>> Please provide a video codec from %s " % mod_cfg.valid_VideoCodec
                    return False

            if outputExt in mod_cfg.valid_imgFileTypes:
                processType = "mov2img"

        return (processType, library)

    @staticmethod
    def validate(args):
        '''
            this verify all the inputs from user end if any input is not as expected, it will through an error and
            stop the process right here

            for how validations are performing you can refer to ./scripts/common/validate.py

            all major validation functionality are present in above path

        '''
        if not mod_validate.Validation.isValid_InputFile(args.inputPath):
            print ">>> invalid input path...!!!"
            return False

        pattern = re.compile("./\.*")
        if pattern.match(str(args.outputPath)):
            basename = str(args.outputPath).split("./")[-1]
            args.outputPath = "/".join([os.path.dirname(args.inputPath), basename])

        if not mod_validate.Validation.isValid_OutputFile(args.outputPath):
            print ">>> invalid output path...!!!"
            return False

        print ">>> input and output verified...!!!"

        if args.frameRange:
            if not mod_validate.Validation.isValid_frameRange(args.frameRange):
                print ">>> invalid Frame range...!!! provide range as -range 1-5,8,10-15"
                return False

        if args.videoCodec:
            if not mod_validate.Validation.isValid_VideoCodec(args.videoCodec):
                print ">>> invalid Video Codec...!!! Use one of  %s " % mod_cfg.valid_VideoCodec
                return False
            if args.videoCodec == "photojpeg":
                args.videoCodec = "mjpeg"

        if args.scale:
            if not mod_validate.Validation.isValid_ScaleValue(args.scale):
                print ">>> invalid scale value...!!! Enter Percent Value between 1-500, 100% is the current scale"
                return False

        if args.width:
            if not mod_validate.Validation.isValid_ResFactor(args.width):
                print ">>> invalid width...!!!", args.width
                return False

        if args.height:
            if not mod_validate.Validation.isValid_ResFactor(args.height):
                print ">>> invalid height...!!!", args.height
                return False

        args.aspectRatio = None
        if args.resolution:
            if not mod_validate.Validation.isValid_Resolution(str(args.resolution)):
                print ">>> invalid resolution...!!!, Please enter as -res 1920x1080 "
                return False

            args.width, args.height = str(args.resolution).split("x")
            args.aspectRatio = float(args.width)/float(args.height)

        if args.textData:

            if not mod_validate.Validation.isValid_FontSize(args.textSize):
                print ">>> invalid font size...!!!, Please enter font size between 1 to 999"
                return False

            if not mod_validate.Validation.isValid_FontFamily(args.textFontFamity):
                print ">>> invalid Font family...!!!, Please choose any from ", mod_cfg.valid_fontsName
                return False

            if not mod_validate.Validation.isValid_FontColor(args.textColor):
                print ">>> invalid Font Color...!!!, Please Enter color in RGB as (255, 255, 255) ."
                return False

            if not mod_validate.Validation.isValid_FontPos(args.textPosition):
                print ">>> invalid Font Position...!!!, Please Enter Text Pos in XY as (1280, 720) ."
                return False

            if not mod_validate.Validation.isValid_TextOpacity(args.textOpacity):
                print ">>> invalid Font Opacity...!!!, Please Enter Text Opacity between 1-100."
                return False


        return args


def main():
    '''
    this is for example
    note :  If you are calling this method via any other application like Maya/Nuke,

        > You have to create a dictionary with arguments (check parser.py for more information about arguments)

        > Once You have created dictionary in your app, convert it to argparse.namespace()
            for converting dict to argparse.namespace(), I've created a method in general module
            where you can pass the dict and it will return the namespace object. check below code.

            import scripts.common.general as mod_general
            arguments = mod_general.dict_to_namespace(myDictionary)

        :: argparse.namespace is the fastest way to store/access any class attributes, that's why namespace has been used.

        > then pass the arguments variable to Transcode Class as args.

    '''
    arguments = mod_parser.TerminalParser.parseInfo(mod_cfg)
    #print arguments
    obj = Transcode(arguments)
    obj.process()

