# You shouldn't need to run this script manually
# It is only used during the creation of VSCode devcontainers
SCRIPTS_DIR=$(dirname "$0")
DEVCONTAINER_DIR=${SCRIPTS_DIR}/..
PROJECT_DIR=${DEVCONTAINER_DIR}/..

rm ${PROJECT_DIR}/.env
[ -f ${PROJECT_DIR}/.env.bak ] && mv ${PROJECT_DIR}/.env.bak ${PROJECT_DIR}/.env
