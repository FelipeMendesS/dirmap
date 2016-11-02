bind '"\e[A":history-search-backward'
bind '"\e[B":history-search-forward'

export EDITOR="vi"
export CLICOLOR=1
export XCODE="`xcode-select --print-path`"
#export PATH="/Users/CHOCK/bin:$PATH\
#:/opt/local/bin:/opt/local/sbin"
function cd {
	builtin cd "$@" && ls -F

}
source ~/.bashrc

# added by Anaconda 2.1.0 installer
export PATH="/Users/FelipeMendes/anaconda/bin:$PATH"


export CS61B_LIB_DIR="/Users/FelipeMendes/UCBerkeley/cs61b/bgl/lib/*"
export CLASSPATH="$CLASSPATH:$CS61B_LIB_DIR:./"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

export PATH="/usr/local/gcc-arm-none-eabi-4_9-2015q1/bin/:$PATH"
export PATH="~/Developing/pick/:$PATH"

# Your previous /Users/FelipeMendes/.bash_profile file was backed up as /Users/FelipeMendes/.bash_profile.macports-saved_2015-02-24_at_13:49:30
##

# MacPorts Installer addition on 2015-02-24_at_13:49:30: adding an appropriate PATH variable for use with MacPorts.
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
# Finished adapting your PATH environment variable for use with MacPorts

test -r /sw/bin/init.sh && . /sw/bin/init.sh

source ~/.git-completion.bash

##
# Your previous /Users/FelipeMendes/.bash_profile file was backed up as /Users/FelipeMendes/.bash_profile.macports-saved_2015-10-20_at_10:42:55
##

# MacPorts Installer addition on 2015-10-20_at_10:42:55: adding an appropriate PATH variable for use with MacPorts.
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
# Finished adapting your PATH environment variable for use with MacPorts.

