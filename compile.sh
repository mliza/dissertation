# Auxiliary function used to handle submodules
gitSubmodule() {
    if [ ! -d "configuration/myResources/Latex" ]; then
        git submodule update --init --recursive
    else
        git submodule update --remote configuration/myResources
    fi
}

# Auxiliary function used to compile dissertation
compileLatex() {
    pdflatex $1.tex;
    makeindex $1.nlo -s nomencl.ist -o $1.nls;
    biber $1;
    pdflatex $1.tex; 
    rm $1.aux $1.bbl $1.bcf $1.blg $1.glo* $1.gls* $1.ist $1.log $1.out $1.run.xml $1.slg $1.slo $1.sls $1.tdo $1.toc $1.glg* $1.lot $1.lof $1.dvi;
}

gitSubmodule
compileLatex main
