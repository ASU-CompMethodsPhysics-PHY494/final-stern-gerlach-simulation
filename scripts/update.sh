#!/bin/bash
# Update the PHY 494 Final Repository.
#
# Oliver Beckstein 2016, placed into the public domain

progname="$0"
REMOTE_NAME="skeleton"
REMOTE_URL="https://github.com/ASU-CompMethodsPhysics-PHY494/Final_Project.git"

function die () {
    local msg="$1" err=${2:-1}
    echo "ERROR: ${msg}"
    exit $err
}

function set_remote () {
    local NAME="$1" URL="$2"
    if ! git remote get-url ${NAME} >/dev/null 2>&1; then
	echo "Adding remote repository '${NAME}'."
	git remote add ${NAME} ${URL}
    fi
}

set_remote ${REMOTE_NAME} ${REMOTE_URL}
    

echo "updating repository... git pull from ${REMOTE_NAME}"
git pull ${REMOTE_NAME} master

topdir="$(git rev-parse --show-toplevel)" || die "Failed to get rootdir"
cd "${topdir}" || die "Failed to get to the git root dir ${rootdir}"

echo "creating subdirectories (if any are missing)"
for subdir in Grade Submission Work docs poster; do
    newdir="${subdir}"
    test -d "${newdir}" || \
	{ mkdir "${newdir}" && echo "created ${newdir}"; }
done

