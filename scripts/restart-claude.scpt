#! /usr/bin/osascript

-- Restart Claude Desktop application

tell application "Claude"
	quit
end tell

-- Wait for the app to fully close
delay .5

-- Reopen Claude
tell application "Claude"
	activate
end tell