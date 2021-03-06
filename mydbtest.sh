clear

BTREE="btree"
HASH="hash"
INDEX="indexfile"

if [ "$#" -ne 1 ]; then
    echo "Program takes 1 argument: "
    echo "btree, hash, or indexfile"

elif [ "$1" == $BTREE ]; then
    python3 dbBTree.py

elif [ "$1" == $HASH ]; then
    python3 dbHash.py

elif [ "$1" == $INDEX ]; then
    python3 dbIndex.py

else
    echo "Argument must be: btree, hash, or indexfile! "
fi
