function port_files() {
    files=$(find . -name \*.md)
    for source in $files ; do
        target="${source%.md}.rst"
        tmp="${source%.md}.rst.tmp"
        echo "gupdating: $source to $target"
        m2r $source &&\
            mv $target $tmp &&\
            git mv $source $target &&\
            mv $tmp $target
    done
}
