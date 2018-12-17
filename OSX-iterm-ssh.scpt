tell application "iTerm"
    activate
    delay 1
    create window with default profile
    tell current session of current window
        split horizontally with default profile command "bash -l"
        split vertically with default profile command "bash -l"
        split vertically with default profile command "bash -l"
        split vertically with default profile command "bash -l"
        
    end tell
end tell

tell application "iTerm"
    activate
    tell current session of current window
        write text "ssh -l USERNAME 1.2.3.4"
        write text "sudo -i"
    end tell
end tell


tell application "System Events" to key code 30 using {command down}
tell application "iTerm"
    activate
    tell current session of current window
        write text "ssh -l USERNAME 1.2.3.4"
        write text "sudo -i"
    end tell
end tell

tell application "System Events" to key code 30 using {command down}
tell application "iTerm"
    activate
    tell current session of current window
        write text "ssh -l USERNAME 1.2.3.4"
        write text "sudo -i"
    end tell
end tell

tell application "System Events" to key code 30 using {command down}
tell application "iTerm"
    activate
    tell current session of current window
        write text "ssh -l USERNAME 1.2.3.4"
        write text "sudo -i"
    end tell
end tell

tell application "System Events" to key code 30 using {command down}
tell application "iTerm"
    activate
    tell current session of current window
        write text "ssh -l USERNAME 1.2.3.4"
        write text "sudo -i"
    end tell
end tell


