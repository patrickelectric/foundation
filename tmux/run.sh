TMUX_FOLDER="$HOME/.tmux"

if [ ! -f "$TMUX_FOLDER/bash_utils.sh" ]; then
    echo "Create tmux folder and necessary scripts.."
    REPO=https://github.com/patrickelectric/foundation/raw/master
    mkdir -p "$TMUX_FOLDER"
    wget $REPO/sh/utils.sh -O "$TMUX_FOLDER/bash_utils.sh"
    wget $REPO/tmux/run.sh -O "$TMUX_FOLDER/run.sh"
    wget $REPO/tmux/.tmux.conf -O "$TMUX_FOLDER/.tmux.conf"
    wget $REPO/simple_tools/computer_info.py -O "$TMUX_FOLDER/computer_info.py"
    chmod +x "$TMUX_FOLDER/computer_info.py"
fi

if [ ! -f "$TMUX_FOLDER/run.sh" ]; then
    echo "SOMETHING IS WRONG!"
    echo "No tmux folder or bash scripts."
    echo "Restart script again."
    exit 1
fi

source "$TMUX_FOLDER/bash_utils.sh"

checktool "command -v crontab" "Crontab exist." "Please, install crontab. (cronie)"
if [ -f "$HOME/tmux.conf" ]; then
    runstep "cp $HOME/tmux.conf $HOME/tmux.conf.backup" "Tmux configuration file backup created" "Failed to create a backup of tmux configuration file"
fi
runstep "mv $TMUX_FOLDER/.tmux.conf $HOME/.tmux.conf" "Moved new tmux configuration file" "Failed to move tmux configuration file"
echob "You can run '$TMUX_FOLDER/run.sh' to update theme and scripts."

runstep "curl -s wttr.in/$(curl -s http://ip-api.com/csv\?fields\=city)\?format\="%c%20%t%20%w" > /tmp/tmux.wttr" "Create weather file" "Failed to create weather file"

echob "Add the following line in cron ('crontab -e')"
echo '*/5 * * * * curl -s wttr.in/$(curl -s http://ip-api.com/csv\?fields\=city)\?format=\%c\%20\%t\%20\%w > /tmp/tmux.wttr'
