__author__ = 'arjun_prasad_namdeo'

import os
import subprocess
import re

import config as mod_cfg


def get_Files_By_Type(inputDirectory=None, fileExtensions=None):
    '''
    @param inputDirectory: the path of directory where you want to find the files
    @param fileExtensions: file extension for valid files in the directory
    @return: it returns a generator where you can iterate items in that
                returns empty generator if nothing found or invalid directory
    '''

    if not inputDirectory:
        return

    if not os.path.isdir(inputDirectory) or not os.listdir(inputDirectory):
        return

    for file in os.listdir(inputDirectory):
        if file.endswith(fileExtensions):
            filePath = os.path.join(inputDirectory, file)
            yield filePath

def get_file_extension(filePath):
    return os.path.splitext(filePath)[-1]

def setDirectory(directoryPath):
    try:
        os.makedirs(directoryPath)
    except OSError:
        if not os.path.isdir(directoryPath):
            raise

def run_in_terminal(command):
    if mod_cfg.os_family == "Windows":
        subprocess.call(command)
    else:
        os.system(command)

def get_seq_padding_count_from_outputString(filePath):
    count = None
    if "#" in filePath:
        seq_pad = re.search("#+", filePath).group(0)
        count = len(seq_pad)
    elif "%" in filePath:
        seq_pad = re.search("%\d+d", filePath).group(0)
        count = int(seq_pad.split("%")[-1])

    return count



def get_seq_padding_count_from_filePath(filePath):
    import pyseq
    all_seqs = pyseq.get_sequences(os.path.dirname(filePath))
    basename = os.path.basename(filePath).split("#")[0]
    basename = basename.split("%")[0]

    for seq in all_seqs:
        stringFormat = seq.format('%h')
        if not str(basename) == str(stringFormat):
            continue

        if seq.missing():
            print ">>> Total Frame Range found : ",  seq.format('%r')
            print ">>> Missing Frames found    : ", seq.missing()
            continue

        if not re.search("%\d+d", seq.format('%p')):
            return False
        framePad = re.search("%\d+d", seq.format('%p')).group(0)
        return int(re.search("\d+", framePad).group(0))


def get_seq_name_from_filePath(filePath, lib="ffmpeg"):
    dir_path = os.path.dirname(filePath)
    framePadding = get_seq_padding_count_from_filePath(filePath)
    if not framePadding:
        print ">>> Invalid Sequence Padding...!! Please use as image.%04d.tga or image.####.tga"
        return False

    import pyseq
    all_seqs = pyseq.get_sequences(dir_path)
    basename = os.path.basename(filePath).split("#")[0]
    basename = basename.split("%")[0]

    for seq in all_seqs:
        stringFormat = seq.format('%h')
        if not str(basename) == str(stringFormat):
            continue

        if seq.missing():
            print ">>> Total Frame Range found : ",  seq.format('%r')
            print ">>> Missing Frames found    : ", seq.missing()
            continue

        if lib == "ffmpeg":
            seq_renders = "{0}{1}{2}".format(seq.format('%h'), seq.format('%p'), seq.format('%t'))

        if lib == "djv":
            seq_renders = set_seq_padding(seq.format('%h'), seq.format('%r'), framePadding, seq.format('%t'))

        return "/".join([dir_path, seq_renders])

    print ">>> No image sequence found as mentioned...!!!"
    return False


def set_seq_padding(imageBaseName="render", frameRange="1-5", paddingCount=4, extension=".dpx"):
    if "-" in str(frameRange):
        st_frame = str(str(frameRange).split("-")[0]).zfill(int(paddingCount))
        end_frame = str(str(frameRange).split("-")[1]).zfill(int(paddingCount))
        seq_string = "{0}{1}-{2}{3}".format(imageBaseName, st_frame, end_frame, extension)
    else:
        seq_string = "{0}{1}{2}".format(imageBaseName, frameRange, extension)
    return seq_string


def namespace_to_dict(namespaceDict):
    return vars(namespaceDict)

def dict_to_namespace(dict):
    import argparse
    args = argparse.Namespace()
    tmp_dict = {'videoCodec': None, 'frameRate': mod_cfg.fps, 'height': None, 'outputPath': None, 'width': None,
            'scale': None, 'frameRange': None, 'inputPath': None, 'resolution': None}
    namespace_dict = vars(args)
    namespace_dict.update(tmp_dict)
    namespace_dict.update(dict)
    return args

def get_font_path():
    fontPath = mod_cfg.packagePath + "/bin/fonts"
    if mod_cfg.os_family == "Windows":
        modify_fontPath = fontPath.replace("\\", "\\\\")
        modify_fontPath = modify_fontPath.replace(":\\", "\\:\\")
        return (fontPath, modify_fontPath)

    return (fontPath, fontPath)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
