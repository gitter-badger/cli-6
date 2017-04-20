#!/bin/bash
#############################################################################
# Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
# Author <jacoby@sparkl.com> Jacoby Thwaites.
#############################################################################
#
# CLI wrapper for SPARKL REST interface. See help.
#
# Arguments are positional, optional arguments come after mandatory ones.
# Each command is separately documented below.

#############################################################################
# Checks mandatory arguments are provided, and total arg count is
# not exceeded.
# usage <actual_count> <mandatory_count> <optional_count> <help_string>
#############################################################################
usage() {
  local COUNT=$1
  local MANDATORY=$2
  local OPTIONAL=$3
  local USAGE=$4
  local MAXIMUM=$(($MANDATORY + $OPTIONAL))

  if [[ $COUNT -lt $MANDATORY ]] || [[ $COUNT -gt $MAXIMUM ]]
  then
    echo "Usage: $SELF $CMD $USAGE"
    exit 1
  fi
}

#############################################################################
# Outputs the singleton use pathname.
# RESULT=$(use_file)
#############################################################################
use_file() {
  echo $WORKING_DIR/use
}

#############################################################################
# Outputs the singleton accept pathname.
# RESULT=$(accept_file)
#############################################################################
accept_file() {
  echo "$WORKING_DIR/accept"
}

#############################################################################
# Outputs the connection cookies pathname.
# RESULT=$(cookies_file [connection_name])
#############################################################################
cookies_file() {
  local NAME=${1:-`cat $(use_file)`}

  echo "$WORKING_DIR/$NAME.cookies"
}

#############################################################################
# Outputs the connection url pathname.
# RESULT=$(url_file [connection_name])
#############################################################################
url_file() {
  local NAME=${1:-`cat $(use_file)`}

  echo "$WORKING_DIR/$NAME.url"
}

#############################################################################
# Outputs the connection cwd pathname.
# RESULT=$(cwd_file)
#############################################################################
cwd_file() {
  local NAME=${1:-`cat $(use_file)`}

  echo "$WORKING_DIR/$NAME.cwd"
}

#############################################################################
# Outputs the current base url.
# RESULT=$(base_url)
#############################################################################
base_url() {
  cat $(url_file)
}

#############################################################################
# Outputs the client's current working folder in the SPARKL config tree.
# RESULT=$(pwd)
#############################################################################
get_pwd() {
  cat $(cwd_file)
}

#############################################################################
# Outputs true if connection_name has been opened, otherwise false.
# RESULT=$(is_open foo)
#############################################################################
is_open() {
  local NAME=$1

  if [ -f $WORKING_DIR/$NAME.url ]; then
    echo "true"
  else
    echo "false"
  fi
}

#############################################################################
# Outputs the name of the connection in use, or "" if none.
# RESULT=$(in_use)
#############################################################################
in_use() {
  if [ -f $(use_file) ]; then
    cat $(use_file)
  else
    echo ""
  fi
}

#############################################################################
# Succeeds if deps are present, otherwise exits with error.
#############################################################################
assert_deps() {
  local DEP
  local MISSING
  for DEP in "curl" "python" "xmllint" "xsltproc"; do
    if ! which $DEP > /dev/null; then
      MISSING="$MISSING $DEP"
    fi
  done

  if [ "$MISSING" != "" ]; then
    echo "Missing dependencies: $MISSING"
    exit 1
  fi
}

#############################################################################
# Succeeds if a connection is in use, otherwise exits with error.
#############################################################################
assert_use() {
  if [ ! -f $(use_file) ]; then
    echo "Must use an open connection first"
    exit 1
  fi
}

#############################################################################
# Succeeds if a user is logged in, otherwise exits with error.
#############################################################################
assert_login() {
  if [ ! -f $(cwd_file) ]; then
    echo "Must login user first"
    exit 1
  fi
}

#############################################################################
# Outputs the path obtained by resolved the href against the (optional)
# base. If no base is supplied, the current client folder is used.
# resolve <href> [base]
#############################################################################
resolve() {
  local HREF=$1
  local BASE=${2:-`get_pwd`}
  local SCRIPT="import os; "
  SCRIPT="$SCRIPT print os.path.normpath(os.path.join('$BASE','$HREF'))"
  echo $(python -c "$SCRIPT")
}

#############################################################################
# Optionally sets, then outputs the current accept header (json or xml)
# and returns success code 0.
# If the new value is invalid, returns error code 1.
# RESULT=$(current_accept [xml|json])
#############################################################################
accept() {
  local NEW_VALUE="$1"
  local ACCEPT_FILE=$(accept_file)

  if [ "$NEW_VALUE" = "" ]; then
    if [ -f "$ACCEPT_FILE" ]; then
      cat $ACCEPT_FILE
    else
      echo "accept:application/json"
    fi

  elif [ "$NEW_VALUE" = "json" ]; then
    echo "accept:application/json" > $ACCEPT_FILE

  elif [ "$NEW_VALUE" = "xml" ]; then
    echo "accept:application/xml" > $ACCEPT_FILE

  else
    return 1
  fi
}

#############################################################################
# Outputs the result of a curl using the specified URL and params.
# Cookies and formatting are handled automatically.
#
# If the env var $DEBUG is non-empty, then the curl command is echoed to
# stderr sans output control args. Just copy and paste this to test it.
#
# The curl failure code is returned (0 for success).
# do_curl <get|post> <default|xml|json> <url> [curl_args..]
#############################################################################
do_curl() {
  local METHOD=$1
  local FORMAT=${2:-user}
  local URL=$3
  shift 3
  local ARGS=$@
  local RESPONSE=`mktemp`

  case $METHOD in
    post|POST)
      case $* in
        *"-d "*)
          ;;

        *"--data"*)
          ;;

        *)
          ARGS="$ARGS --data ''"
          ;;
      esac
      ;;

    get|GET)
      ARGS="$ARGS --get"
      ;;
  esac

  case $FORMAT in
    user)
      ARGS="$ARGS --header $(accept)"
      ;;

    json|JSON)
      ARGS="$ARGS --header accept:application/json"
      ;;

    xml|XML)
      ARGS="$ARGS --header accept:application/xml"
      ;;
  esac

  ARGS="$ARGS --cookie-jar $(cookies_file)"
  ARGS="$ARGS --cookie $(cookies_file)"
  ARGS="$ARGS --silent"

  if [ "$DEBUG" = "true" ]; then
    >&2 echo
    >&2 echo "curl $ARGS $URL"
    >&2 echo
  fi

  ARGS="$ARGS --write-out %{http_code}"
  ARGS="$ARGS --output $RESPONSE"

  local HTTP_CODE=`curl $ARGS $URL`
  local CURL_STATUS=$?

  # We generate output if response received.
  if [ $CURL_STATUS -eq 0 ]; then

    # Pretty print for user, otherwise leave unchanged.
    if [ "$FORMAT" = "user" ]; then
      if [ $(accept) = "accept:application/json" ]; then
        python -m json.tool $RESPONSE
      elif [ $(accept) = "accept:application/xml" ]; then
        xmllint --format $RESPONSE
      fi
    else
      cat $RESPONSE
    fi
  fi

  rm $RESPONSE

  if [ $CURL_STATUS -eq 0 ] && [ $HTTP_CODE -eq 200 ]; then
    return 0
  else
    return 1
  fi
}

#############################################################################
# Performs a garbage collection on the working directory parent, removing
# all client directories whose name does not match a running process.
#############################################################################
gc() {
  local PID
  for PID in $(ls $TMPDIR/sse_cli); do
    if ! ps -p $PID > /dev/null; then
      rm -rf $TMPDIR/sse_cli/$DIR
    fi
  done
}

#############################################################################
# Sets the accepted response to JSON or XML.
# cmd_accept <xml|json>
#############################################################################
cmd_accept() {
  local FORMAT=$1

  accept $FORMAT
}

#############################################################################
# Changes the current working SPARKL config folder.
# cmd_cd <href>
#############################################################################
cmd_cd() {
  local HREF=$1
  local CWD_FILE=$(cwd_file)
  local CONTENT_URL="$(base_url)/sse_cfg/content"
  local ARGS
  local SCRIPT
  local NEW_CWD

  NEW_CWD=$(resolve $HREF)

  do_curl get xml $CONTENT_URL/$NEW_CWD > /dev/null
  if [ $? -eq 0 ]; then
    echo $NEW_CWD > $CWD_FILE
  else
    echo "No folder $NEW_CWD"
  fi
}

#############################################################################
# Lists the current client status including opened connections and use.
# cmd_client
#############################################################################
cmd_client() {
  local FILE
  local USING=$(in_use)

  if [ "$USING" != "" ]; then
    echo "Using connection '$USING'"
  else
    echo "No connection in use"
  fi

  if [ -f $(use_file) ] && [ -f $(cwd_file) ]; then
    echo "User is logged in"
  else
    echo "Not logged in"
  fi

  echo "Accepting `basename $(accept)`"

  shopt -s nullglob
  for FILE in $WORKING_DIR/*.url; do
    local NAME=`echo $(basename $FILE) | sed s/\.url//`
    echo "Connection '${NAME}' at `cat $(url_file $NAME)`"
  done
}

#############################################################################
# Closes the connection in use by deleting the files.
# cmd_close
#############################################################################
cmd_close() {
  rm $WORKING_DIR/$(in_use).*
  rm $(use_file)
}

#############################################################################
# Gets the source of the named object, resolved relative to cwd.
# cmd_get <name>
#############################################################################
cmd_get() {
  local NAME=$1
  local URL="$(base_url)/sse_cfg/source"
  local OBJECT=$(resolve $NAME)

  do_curl get user $URL/$OBJECT
}

#############################################################################
# Outputs help.
# cmd_help
#############################################################################
cmd_help() {
  echo "SPARKL client"
  echo "Usage: `basename $0` [command [arg..]]"
  echo
  echo "Args are positional. Commands are:"
  echo "  accept   - selects XML or JSON response format"
  echo "  cd       - changes the working folder"
  echo "  client   - (default) shows current client status"
  echo "  close    - closes the connection in use"
  echo "  open     - opens a connection"
  echo "  get      - gets the configuration source of an object"
  echo "  help     - (or invalid command) shows this help"
  echo "  info     - shows information about a specified node"
  echo "  ls       - lists folder contents"
  echo "  login    - logs in the user with email and password"
  echo "  logout   - logs out the current user"
  echo "  ping     - pings the connection in use"
  echo "  put      - applies an XML change to the working folder"
  echo "  pwd      - shows the working folder"
  echo "  register - registers a new user if permitted"
  echo "  undo     - reverses the most recent XML change"
  echo "  use      - uses an opened connection"
  echo "  user     - info about the currently logged in user"
  echo
  echo "Use 'export DEBUG=true' to debug curl invocations."
  echo
}

#############################################################################
# Shows info on the connection node or other node if specified.
# cmd_info <node>
#############################################################################
cmd_info() {
  local NODE=$1
  local URL="$(base_url)/sse/info"
  local ARG="--data node=$NODE"

  do_curl get user $URL $ARG
}

#############################################################################
# Lists the content of the specified or current configuration folder.
# cmd_ls <href>
#############################################################################
cmd_ls() {
  local HREF=$1
  local URL="$(base_url)/sse_cfg/content"
  local OBJECT="$(resolve $HREF)"
  local XSL_FILE="$WORKING_DIR/ls.xsl"

  if [ ! -f $XSL_FILE ]; then
    cat > $XSL_FILE << 'END_OF_XSL'
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text"/>
  <xsl:template match="/content">
    <xsl:for-each select="*">
      <xsl:value-of select="concat(local-name(),'&#9;',@name,'&#xA;')"/>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
END_OF_XSL
  fi

  do_curl get xml $URL/$OBJECT | xsltproc $XSL_FILE -
}

#############################################################################
# Signs in the user, prompting for password if not supplied.
# cmd_login <email> [password]
#############################################################################
cmd_login() {
  local USER=$1
  local PASSWORD=$2
  local URL="$(base_url)/sse_cfg/user"
  local CWD_FILE=$(cwd_file)

  if [ "$PASSWORD" = "" ]; then
    read -s -p "Password: " PASSWORD
    echo
  fi

  USER="--data email=$USER"
  PASSWORD="--data password=$PASSWORD"
  do_curl post user $URL $USER $PASSWORD

  if [ $? -eq 0 ]; then
    echo "/" > $CWD_FILE
  fi
}

#############################################################################
# Logs out the user.
# cmd_logout
#############################################################################
cmd_logout() {
  local URL="$(base_url)/sse_cfg/signout"
  local CWD_FILE=$(cwd_file)

  do_curl post user $URL
  rm $CWD_FILE
}

#############################################################################
# Opens a connection by creating the cookie file and storing the url in
# the url file. Checks the ping returns 200 OK.
# cmd_conn [<connection_name> <url>]
#############################################################################
cmd_conn() {
  local NAME=$1
  local URL=$2
  local COOKIES_FILE=$(cookies_file $NAME)
  local URL_FILE=$(url_file $NAME)
  local PING_URL="$URL/sse/ping"

  curl -s -f -o /dev/null $PING_URL
  if [ $? -eq 0 ]; then
    touch $COOKIES_FILE
    echo "$URL" > $URL_FILE
  else
    echo "No SPARKL at $2"
  fi
}

#############################################################################
# Pings the current connection.
# cmd_ping [node_name]
#############################################################################
cmd_ping() {
  local NODE=$1
  local URL="$(base_url)/sse/ping"

  if [ "$NODE" = "" ]; then
    do_curl get user $URL
  else
    ARG="--data node=$1"
    do_curl get user $URL $ARG
  fi
}

#############################################################################
# Uploads the named file to the current configuration folder.
# cmd_put <file_name>
#############################################################################
cmd_put() {
  local FILE=$1
  local URL="$(base_url)/sse_cfg/change/$(get_pwd)"

  if [ -f $FILE ]; then
    local ARGS="--data-binary @$FILE"
    ARGS="$ARGS --header Content-Type:application/xml"
    ARGS="$ARGS --header x-sparkl-transform:gen_change"
    do_curl post user $URL $ARGS
  else
    echo "No file $FILE"
    exit 1
  fi
}

#############################################################################
# Shows the current working SPARKL config folder.
# cmd_pwd
#############################################################################
cmd_pwd() {
  get_pwd
}

#############################################################################
# Registers a new user, prompting for password if not supplied.
# cmd_register <email> [password]
#############################################################################
cmd_register() {
  local USER=$1
  local PASSWORD=$2
  local URL="$(base_url)/sse_cfg/register"

  if [ "$PASSWORD" = "" ]; then
    read -s -p "Password: " TAKE1
    echo
    read -s -p "Repeat:   " TAKE2
    echo
    if [ "$TAKE1" = "$TAKE2" ]; then
      PASSWORD=$TAKE1
    else
      echo "Passwords differ"
      exit 1
    fi
  fi

  USER="--data email=$USER"
  PASSWORD="--data password=$PASSWORD"
  do_curl post $URL user $USER $PASSWORD

  if [ $? -eq 0 ]; then
    echo "/" > $CWD_FILE
  fi
}

#############################################################################
# Undoes the most recent change.
# cmd_undo
#############################################################################
cmd_undo() {
  echo Undo...
}

#############################################################################
# Sets the named connection to in use.
# cmd_use [connection_name]
#############################################################################
cmd_use() {
  local NAME=$1

  if [ "$(is_open $NAME)" = "true" ]; then
    echo $NAME > $(use_file)
  else
    echo "Must open connection '$NAME' first"
  fi
}

#############################################################################
# Retrieves current logged-in user.
#############################################################################
cmd_user() {
  local URL="$(base_url)/sse_cfg/user"

  do_curl get user $URL
}

#############################################################################
# MAIN ROUTINE
#
# Interprets the command line and dispatches accordingly, honouring the
# function return status code.
#
# Invokes the garbage collection function on each invocation.
#############################################################################
TMPDIR=${TMPDIR:-/tmp}
assert_deps
gc
SELF=`basename $0`
CMD=$1
WORKING_DIR=$TMPDIR/sse_cli/$PPID
mkdir -p $WORKING_DIR
shift
case $CMD in

  accept)
    usage $# 1 0 "<xml|json>"
    cmd_accept $1
    if [ $? -ne 0 ]; then
      usage 0 1 0 "<xml|json>"
    fi
    ;;

  cd)
    usage $# 1 0 "<folder>"
    assert_use
    assert_login
    cmd_cd $1
    ;;

  client|"")
    cmd_client
    ;;

  close)
    usage $# 0 0 ""
    assert_use
    cmd_close
    ;;

  get)
    usage $# 1 0 "<href>"
    assert_use
    assert_login
    cmd_get $1
    ;;

  info)
    usage $# 1 0 "<node_name>"
    assert_use
    assert_login
    cmd_info $1
    ;;

  ls)
    usage $# 0 1 "[href]"
    assert_use
    assert_login
    cmd_ls $1
    ;;

  login)
    usage $# 1 1 "<user> [password]"
    assert_use
    cmd_login $1 $2
    ;;

  logout)
    usage $# 0 0 ""
    assert_use
    assert_login
    cmd_logout
    ;;

  open)
    usage $# 2 0 "<connection_name> <url>"
    cmd_conn $1 $2
    ;;

  ping)
    usage $# 0 1 "[node_name]"
    assert_use
    cmd_ping $1
    ;;

  put)
    usage $# 1 0 "<file_name>"
    assert_use
    assert_login
    cmd_put $1
    ;;

  pwd)
    usage $# 0 0 ""
    assert_use
    assert_login
    cmd_pwd
    ;;

  register)
    usage $# 1 1 "<user> [password]"
    assert_use
    cmd_register $1 $2
    ;;

  undo)
    usage $# 0 0 ""
    assert_use
    assert_login
    cmd_undo
    ;;

  use)
    usage $# 1 0 "<connection_name>"
    cmd_use $1
    ;;

  user)
    usage $# 0 0 ""
    assert_use
    assert_login
    cmd_user
    ;;

  help|*)
    usage $# 0 0 ""
    cmd_help
    ;;
esac
