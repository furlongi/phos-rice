function dnfi --wraps='sudo dnf install' --description 'alias dnfi=sudo dnf install'
  sudo dnf install $argv
  echo "$(tput bold)Installed:$(tput sgr0)"
  sudo dnf list --installed | grep $argv
end
