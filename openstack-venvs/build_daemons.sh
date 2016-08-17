cat ./init.d.tmpl | \
	sed -e "s/#DESC#/${DESC}/g" \
	    -e "s/#PROJECT_NAME#/${PROJECT_NAME}/g" \
	    -e "s/#NAME#/${NAME}/g" \
	    -e "s/#PROVIDES#/${PROVIDES}/g" \
	    -e "s~#CONFIG_FILE#~${CONFIG_FILE}~g" \
	    -e "s~#DAEMON#~${DAEMON}~g" \
	    -e "s~#DAEMON_ARGS#~${DAEMON_ARGS}~g" \
	> $VENV/${PROVIDES}-init.d
chmod +x $VENV/${PROVIDES}-init.d
