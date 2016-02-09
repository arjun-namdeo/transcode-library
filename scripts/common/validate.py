__author__ = 'arjun_prasad_namdeo'

import os
import config as mod_cfg
import re

import scripts.common.general as mod_general

class Validation(object):
    '''
    class docs
    '''

    def __init__(self):
        pass

    @staticmethod
    def isValid_OutputFile(filePath):
        if Validation.isValid_SingleFile(filePath):
            return True

        if os.path.isdir(os.path.dirname(filePath)):
            return Validation.isValid_fileExtension(filePath)
        return False

    @staticmethod
    def isValid_InputFile(filePath):
        if Validation.isValid_SingleFile(filePath):
            return filePath

        return Validation.isValid_Sequence(filePath)

    @staticmethod
    def isValid_SingleFile(filePath):
        if os.path.exists(filePath):
            return Validation.isValid_fileExtension(filePath)

        return False

    @staticmethod
    def isValid_fileExtension(filePath):
        file_ext = os.path.splitext(filePath)
        if file_ext[-1] in list(set(mod_cfg.valid_imgFileTypes + mod_cfg.valid_movFileTypes)):
            return True
        else:
            if len(file_ext[-1]) > 0:
                print ">>> Invalid file extension : ", file_ext[-1]
            return False

    @staticmethod
    def isValid_Sequence(filePath):
        if Validation.isValid_SingleFile(filePath):
            return filePath

        dir_path = os.path.dirname(filePath)
        if not os.path.isdir(dir_path):
            return False

        framePadding = mod_general.get_seq_padding_count_from_filePath(filePath)
        if not framePadding:
            print ">>> Invalid Sequence Padding...!! Please use as image.%04d.tga"
            return False

        return mod_general.get_seq_name_from_filePath(filePath)



    @staticmethod
    def isValid_VideoCodec(codec):
        if str(codec).lower() in mod_cfg.valid_VideoCodec:
            return  True
        return False

    @staticmethod
    def isValid_frameRange(range):
        range_count = []
        for frm in str(range).split(","):
            if str(frm).isdigit():
                range_count.append(frm)
            if "-" in str(frm):
                if not len(str(frm).split("-")) == 2:
                    continue
                st_Frm = str(frm).split("-")[0]
                ed_Frm = str(frm).split("-")[1]

                if str(st_Frm).isdigit() and str(ed_Frm).isdigit():
                    range_count.extend([st_Frm, ed_Frm])

        if range_count:
            return True
        return False

    @staticmethod
    def isValid_ScaleValue(scaleValue):
        valid = False
        try:
            value = float(scaleValue)
            if value < 500 and value > 1:
                valid = True
        except:
            pass

        return valid



    @staticmethod
    def isValid_ResFactor(factor):
        '''
        factor :   pass any number to verify if it's number or not
        '''
        if not str(factor).isdigit():
            return False
        return True

    @staticmethod
    def isValid_Resolution(rez):
        pattern = re.compile("[0-9]+x[0-9]+")
        if not pattern.match(str(rez)):
            return False
        return True


    @staticmethod
    def isValid_FontFamily(fontFamily):
        return fontFamily in mod_cfg.valid_fontsName

    @staticmethod
    def isValid_FontSize(fontSize):
        if not str(fontSize).isdigit():
            return False
        return 0 < fontSize < 999

    @staticmethod
    def isValid_FontColor(fontColor):
        if not len(fontColor) == 3:
            return False
        for color in fontColor:
            if not str(color).isdigit():
                return False
        return True

    @staticmethod
    def isValid_FontPos(fontPos):
        if not len(fontPos) == 2:
            return False
        for pos in fontPos:
            if not str(pos).isdigit():
                return False
        return True

    @staticmethod
    def isValid_TextOpacity(textMix):
        if not str(int(textMix)).isdigit():
            return False
        return 0 < textMix < 101
