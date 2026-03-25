function dnfs --wraps='sudo dnf search' --description 'alias dnfs=sudo dnf search'
  sudo dnf search $argv
  echo "$(tput bold)Installed:$(tput sgr0)"
  sudo dnf list --installed | grep $argv
end
