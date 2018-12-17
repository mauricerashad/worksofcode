#!/bin/bash

# Rotate info and be stateful :)
# Useful when rotating people for notifications weekly, such as in a custom monitoring service / function / script

# Variables
script_name='rotate.sh'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
rotation=('user1' 'thisGuy' 'thatGirl' 'botThing')
count=$(echo ${#rotation[@]} - 1 | bc)
target=/etc/service/conf.d/target.conf
weekdays='monday tuesday wednesday thursday friday saturday sunday'

# The below var is updated each time this script is run so that it remains stateful
# Don't edit manually - just run the script untill the correct rotation is acheived!!!
current_rotation=botThing

# Skip updating target when always
always_rotation='botThing'

# Report rotation and exit
if [ $# -ge 1 ] && [[ $1 != '-F' ]]; then
    printf '%s ' "Pool is ${rotation[@]}" && echo ''
    echo Current rotation is $current_rotation
    echo Argurment \'-F\' will force the run
    [[ $always_rotation != '' ]] && echo Always rotation is $always_rotation
    exit 0
fi

# Run only on Sunday
day=$(date +%a)
if ! [[ $day == Sun ]] && [[ $1 != '-F' ]]; then
    echo Sorry - please run this ONCE on Sunday only
    exit 1
fi

# Only allow root to run
if [[ $EUID -ne 0 ]]; then
   printf "This can only be run as ${RED}root${NC}.\n" 1>&2
   exit 1
fi

for next_rotated_idx in $(seq 0 $count); do
    # If we are at the last element in the array, then the next rotated person is the first element
    if [ $next_rotated_idx -eq $count ]; then
        last_rotated_idx=$next_rotated_idx
        next_rotated_idx=0
        break
    # If this element in the array is current, then the next element in the array is assigned
    elif [[ $current_rotation == "$(echo ${rotation[$next_rotated_idx]})" ]]; then
        last_rotated_idx=$next_rotated_idx
        next_rotated_idx=$((next_rotated_idx + 1))
        break
    fi
done

# Do some work
for weekday in $weekdays; do
    grep -q $(echo ${rotation[next_rotated_idx]}) <<<$always_rotation && break
    echo Doing some work now - please wait
done

# Do some more work
for weekday in $weekdays; do
    grep -q $(echo ${rotation[last_rotated_idx]}) <<<$always_rotation && break
    echo Doing some work now - please wait
done

# Apply changes
service myservice reload

# Stateful update. Update this script to remain stateful
sed -i "/^current_rotation/c current_rotation=${rotation[$next_rotated_idx]}" $DIR/$script_name

# Report on current operations and exit
echo ${rotation[$last_rotated_idx]} has been rotated out
echo ${rotation[$next_rotated_idx]} has been rotated in 

