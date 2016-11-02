export MATLAB_JAVA=/Library/Java/JavaVirtualMachines/jdk1.7.0_71.jdk/Contents/Home/jre/


export CS61B_LIB_DIR="/Users/FelipeMendes/UCBerkeley/cs61b/bgl/lib/*"
export CLASSPATH="$CLASSPATH:$CS61B_LIB_DIR:./"
alias gs='git status'
alias ga='git add'
alias gb='git branch'
alias gc='git commit -a -m'
alias gd='git diff'
alias go='git checkout '
alias gpul='git pull origin master'
alias gpus='git push origin master'

alias g='java Gitlet'
alias sg='java StaffGitlet'

alias pick='pick.sh'


push() {
    git push origin master
    git push origin master:ag/$1
    git push origin master:submit/$1
}

HISTSIZE=5000
HISTIGNORE="jrnl *"
