function zyp --wraps='sudo zypper' --description 'alias zyp=sudo zypper'
  sudo zypper $argv
end
