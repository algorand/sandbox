#BLACK=$(tput setaf 0)
#RED=$(tput setaf 1)
#GREEN=$(tput setaf 2)
#YELLOW=$(tput setaf 3)
#BLUE=$(tput setaf 4)
#PINK=$(tput setaf 5)
#CYAN=$(tput setaf 6)
#WHITE=$(tput setaf 7)
RED=`echo -en "\e[41m"`
GREEN=`echo -en "\e[42m"`
ORANGE=`echo -en "\e[43m"`
BLUE=`echo -en "\e[44m"`
PURPLE=`echo -en "\e[45m"`
AQUA=`echo -en "\e[46m"`
GRAY=`echo -en "\e[47m"`
DARKGRAY=`echo -en "\e[100m"`
DEFAULT=`echo -en "\e[49m"`
red=`echo -en "\e[31m"`
green=`echo -en "\e[32m"`
orange=`echo -en "\e[33m"`
blue=`echo -en "\e[34m"`
purple=`echo -en "\e[35m"`
aqua=`echo -en "\e[36m"`
gray=`echo -en "\e[37m"`
darkgray=`echo -en "\e[90m"`
lightred=`echo -en "\e[91m"`
lightgreen=`echo -en "\e[92m"`
lightyellow=`echo -en "\e[93m"`
lightblue=`echo -en "\e[94m"`
lightpurple=`echo -en "\e[95m"`
lightaqua=`echo -en "\e[96m"`
white=`echo -en "\e[97m"`
default=`echo -en "\e[39m"`



function executeUntil {
  while true; do
    read response
    if [[ $response == $1 ]]; then
      return
    else
      eval $response
    fi
  done
}

function execute {
  echo "Running command: ${green}${BLACK}$1${DEFAULT}${default}"
  eval $1
}

cat << EOF
In this tutorial you will use goal to create a wallet, create two accounts in
the wallet, request Algos from the bank, and send Algos between your accounts.

To run this tutorial you will need a testnet sandbox with a fully processed
ledger. If you haven't done that, you can run the command:
${red}'./sandbox up testnet --use-snapshot'${default}

How to use this tutorial
${red}----------------------${default}

This is an interactive tutorial which follows a number of commands designed to
complete the task. Each command is a step of the tutorial and will contain an
explanation of what will happen, followed by the command in square brackets.

When prompted with the next command, any line you enter in the script will be
executed. This is so you can experiment with what is being explained. When
finished, enter an empty line to execute the provided command.
${red}----------------------${default}

Interacting with the Key Management Daemon.

Algorand accounts are secured inside a wallet and managed by a key management
daemon, named KMD. You can interact with KMD using the 'goal' command. Lets
check if there are any wallets registered with your node:

${aqua}[./sandbox goal wallet list]${default}
EOF

executeUntil ""
execute "./sandbox goal wallet list"

cat << EOF
${red}----------------------${default}

Creating a wallet.

That command probably wasn't very interesting, lets create a wallet.

${aqua}[./sandbox goal wallet new test-wallet]${default}

EOF

executeUntil ""
execute "./sandbox goal wallet new test-wallet"

cat << EOF
${red}----------------------${default}

Listing your wallet(s).

Now we can list the wallets and see something more interesting. Try creating a"
couple and see how the results change.

${aqua}[./sandbox goal wallet list]${default}

EOF

executeUntil ""
./sandbox goal wallet list

cat << EOF
${red}----------------------${default}

Creating an account.

Now that we have a wallet (and hopefully set it as the default wallet), we can
create some accounts.

${aqua}[./sandbox goal account new ; ./sandbox goal account new]${default}

EOF

executeUntil ""
execute "./sandbox goal account new ; ./sandbox goal account new"

cat << EOF
${red}----------------------${default}

Listing the accounts.

Similar to how you would list your wallets, you can list your accounts.

${aqua}[./sandbox goal account list]${default}

EOF

executeUntil ""
execute "./sandbox goal account list"

cat << EOF
${red}----------------------${default}

Using the Bank.

A Bank service is available to dispense Algos on Algorand test networks. Try
using one of them to fund one of your accounts:

https://bank.testnet.algorand.network/

Once funded, you can list your accounts to see that the balance has changed. Be
aware that it takes several seconds for a block to be created, so you may need
to wait a moment. Try running the command yourself a couple times until the
Bank transaction has been confirmed.

${aqua}[./sandbox goal account list]${default}

EOF
executeUntil ""
execute "./sandbox goal account list"

# TODO: Capture the output of 'goal account list' to ensure that an account has
#       been funded, and record the addresses for use in the next command.

cat << EOF
${red}----------------------${default}

Making a transaction.

You should now be the proud owner of 100000000 microAlgos, lets try to create
a transaction with them. You'll need to help out with this one, I can't seem to
recall which account you funded. Fill in the blanks on this command to create a
transaction then list your accounts to see that the balances have been updated:

./goal clerk send -a <amount-of-microAlgos> -f <from-account> -t <to-account>

${aqua}[./sandbox goal account list]${default}

EOF

executeUntil ""
execute "./sandbox goal account list"
