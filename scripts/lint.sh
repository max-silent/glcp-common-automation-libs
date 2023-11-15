#!/bin/bash -ex

LIBS_DIR="automation_libs"


if [ -z "${MYPY_DISABLED}" ]; then
  if [ -z ${MYPY_SRC_DIRS+x} ]; then
    MYPY_SRC_DIRS=$LIBS_DIR
  fi
  echo "Running mypy checks for source code in ${MYPY_SRC_DIRS} with directory context $(pwd)"

  eval "arr=($MYPY_SRC_DIRS)"
  for src_dir in "${arr[@]}"; do
      [ ! -d ./${src_dir} ] \
          && echo "Directory ${src_dir} not present" \
          && exit 1
  done

  if [ -z ${MYPY_ARGS+x} ]; then
    MYPY_ARGS="--ignore-missing-imports --module"
  fi

  mypy ${MYPY_ARGS} ${MYPY_SRC_DIRS}
  echo "Done with mypy"
fi

# black code
if [ -z "${BLACK_DISABLED}" ]; then
  if [ -z ${BLACK_SRC_DIRS+x} ]; then
    BLACK_SRC_DIRS=$LIBS_DIR
  fi
  echo "Running black checks for source code in ${BLACK_SRC_DIRS} with directory context $(pwd)"

  eval "arr=($BLACK_SRC_DIRS)"
  for src_dir in "${arr[@]}"; do
      [ ! -d ./${src_dir} ] \
          && echo "Directory ${src_dir} not present" \
          && exit 1
  done

  if [ -z ${BLACK_ARGS+x} ]; then
    BLACK_ARGS="--check --diff --line-length 90"
  fi

  black ${BLACK_ARGS} ${BLACK_SRC_DIRS}
  echo "Done with black"
fi

# isort code
if [ -z "${ISORT_DISABLED}" ]; then
  if [ -z ${ISORT_SRC_DIRS+x} ]; then
    ISORT_SRC_DIRS=$LIBS_DIR
  fi
  echo "Running isort checks for source code in ${ISORT_SRC_DIRS} with directory context $(pwd)"

  eval "arr=($ISORT_SRC_DIRS)"
  for src_dir in "${arr[@]}"; do
      [ ! -d ./${src_dir} ] \
          && echo "Directory ${src_dir} not present" \
          && exit 1
  done

  if [ -z ${ISORT_ARGS+x} ]; then
    ISORT_ARGS="--check-only -l 90 -m 3 --up"
  fi

  isort ${ISORT_ARGS} ${ISORT_SRC_DIRS}
  echo "Done with isort"
fi
