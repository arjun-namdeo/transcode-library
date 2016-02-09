__author__ = 'ArjunPrasadNamdeo'

'''

    If you are using terminal then you have to call this caller.py module

    for Linux and Mac

        $ python /TranscodeSystem/caller.py -h

    for Windows

        C:\python.exe C:\TranscodeSystem\caller.py -h


'''

import transcodeAPI as mod_transcodeAPI
reload(mod_transcodeAPI)

mod_transcodeAPI.main()