import os
import stat

script_fn = "/home/{0}/.local/share/nautilus/scripts/Download subtitles".format(os.getlogin())
script_contents = "#!/bin/bash\n\npython {0}/subbot.py \"$1\""

open(script_fn, "wb").write(script_contents.format(os.path.dirname(os.path.realpath(__file__))))
os.chmod(script_fn, stat.S_IWUSR | stat.S_IRUSR | stat.S_IEXEC)