# You shouldn't need to run this script manually
# It is only used during the creation of VSCode devcontainers
SCRIPTS_DIR=$(dirname "$0")
DEVCONTAINER_DIR=${SCRIPTS_DIR}/..
PROJECT_DIR=${DEVCONTAINER_DIR}/..

[ -f ${PROJECT_DIR}/.env ] && cp ${PROJECT_DIR}/.env ${PROJECT_DIR}/.env.bak
cp ${DEVCONTAINER_DIR}/.env ${PROJECT_DIR}/.env
