#!/bin/bash

# Functions ==============================================

# return 1 if global command line program installed, else 0
# example
# echo "node: $(program_is_installed node)"
function program_is_installed {
  # set to 1 initially
  local return_=1
  # set to 0 if not found
  type $1 >/dev/null 2>&1 || { local return_=0; }
  # return value
  echo "$return_"
}

# return 1 if local npm package is installed at ./node_modules, else 0
# example
# echo "gruntacular : $(npm_package_is_installed gruntacular)"
function npm_package_is_installed {
  # set to 1 initially
  local return_=1
  # set to 0 if not found
  ls ~/.npm | grep $1 >/dev/null 2>&1 || { local return_=0; }
  # return value
  echo "$return_"
}

# display a message in red with a cross by it
# example
# echo echo_fail "No"
function echo_fail {
  # echo first argument in red
  printf "\e[31mx ${1}"
  # reset colours back to normal
  #echo "\033[0m"
}

# display a message in green with a tick by it
# example
# echo echo_fail "Yes"
function echo_pass {
  # echo first argument in green
  printf "\e[32m✔ ${1}"
  # reset colours back to normal
  #echo "\033[0m"
}

# echo pass or fail
# example
# echo echo_if 1 "Passed"
# echo echo_if 0 "Failed"
function echo_if {
  if [ $1 == 1 ]; then
    echo_pass $2
  else
    echo_fail $2
  fi
}

# ============================================== Functions

  if [ $(program_is_installed ethereum) == 1 ]; then
    echo_pass "Ethereum"
  else
    echo "===============Installing Ethereum================="
    apt-get install software-properties-common
    add-apt-repository -y ppa:ethereum/ethereum-qt
    add-apt-repository -y ppa:ethereum/ethereum
    apt-get update
    apt-get install ethereum -y
  fi

  if [ $(program_is_installed nodejs) == 1 ]; then
    echo_pass "Nodejs"
  else
    echo "===============Installing NodeJS 5.x================="
    apt-get install -y nodejs
  fi

    if [ $(program_is_installed avahi-utils) == 1 ]; then
    echo_pass "avahi-utils"
  else
    echo "===============Installing avahi-utils================="
    apt-get install -y avahi-utils
  fi


    if [ $(npm_package_is_installed solc) == 1 ]; then
    echo_pass "Solidity"
  else
    echo "===============Installing Solididty compiler================="
    npm install solc -g
  fi

     if [ $(npm_package_is_installed truffle) == 1 ]; then
    echo_pass "truffle"
  else
    echo "===============Installing truffle================="
    npm install truffle -g
  fi

# command line programs
echo "node          $(echo_if $(program_is_installed node))"
echo "ethereum         $(echo_if $(program_is_installed ethereum))"
echo "avahi-utils         $(echo_if $(program_is_installed avahi-utils))"


# local npm packages
echo "solc   $(echo_if $(npm_package_is_installed solc))"
echo "truffle $(echo_if $(npm_package_is_installed truffle))"