
ORIGINAL=$HOME/Dropbox/Evernote_original

for folder in ICM Master old_stack Lionel-Groulx Personnel
# for folder in Master old_stack Lionel-Groulx Personnel
do
    echo "-" $folder
    mkdir -p notes/$folder
    cd notes/$folder

    for file_html in $ORIGINAL/$folder/*.html
    do
        echo  "---" $file_html
        python3 ../../html2md.py "$file_html"
    done
    cd ../../
done
