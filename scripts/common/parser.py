__author__ = 'arjun_prasad_namdeo'

import argparse

class TerminalParser(object):
    '''
    In here put all the parser related to transcode system.
    '''
    @staticmethod
    def parseInfo(cfg):
        '''
        this will parse the information from terminal and return a argparse.namespace object to the caller

        '''

        parser = argparse.ArgumentParser()
        parser.add_argument('-in', '--inputPath', type=str, help='provide input path', required=True)
        parser.add_argument('-out', '--outputPath', type=str, help='provide output path', required=True)
        parser.add_argument('-vc', '--videoCodec', type=str, help='specify video codec')
        parser.add_argument('-rx', '--width', type=int, help='specify width, this will preserve the Input Pixel Aspect Ratio..!!!')
        parser.add_argument('-ry', '--height', type=int, help='specify height, this will preserve the Input Pixel Aspect Ratio..!!!')
        parser.add_argument('-res', '--resolution', type=str, help='define resolution as -res 1920x1080')
        parser.add_argument('-scale', '--scale', type=str, help='provide Percent Value between 1-500, 100%% is the current scale')
        parser.add_argument('-fps', '--frameRate', type=float, help='provide input path', default=cfg.fps)
        parser.add_argument('-frameRange', '--frameRange', type=str, help='provide Frame range as 1-5,8,11-18')
        parser.add_argument('-text', '--textData', type=str, help='provide Text to write in double quotes as -text "Hello World" ', default=None)
        parser.add_argument('-textMix', '--textOpacity', type=float, help='provide Text Opacity Percentage', default=cfg.textOpacity)
        parser.add_argument('-textSize', '--textSize', type=int, help='provide Text Size between 1-999', default=cfg.textSize)
        parser.add_argument('-textFont', '--textFontFamity', type=str, help='provide choose font from %s ' % cfg.valid_fontsName, default=cfg.textFont)
        parser.add_argument('-textColor', '--textColor', type=int, nargs=3,  help='provide Text Color in RGB as -textColor 255 255 255', default=cfg.textColor)
        parser.add_argument('-textPos', '--textPosition', type=int, nargs=2,  help='provide Text Pixel Position as -textPos 1280 720 ', default=cfg.textPos)

        return parser.parse_args()


