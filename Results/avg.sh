for file in *.dat
do
    sum=0
    num_lines=0
    while read line
    do
        sum=$(bc <<< "scale=6;$line + $sum") 
        let num_lines+=1
    done < $file
    filename=$(basename $file .dat)
    sum=$(bc <<< "scale=6;$sum/$num_lines") 
    ps=${filename:2:1}
    dos=${filename:4:1}
    flows=${filename:6:1}
    #echo "PS: $ps , D: $dos , F: $flows"
    #echo "$file: $sum"
    echo "$ps $dos $sum" >> bench.dat
done
