gui := squall/gui
widgets := $(wildcard $(gui)/*.ui)

interfaces: $(widgets:$(gui)/%.ui=$(gui)/Ui_%.py) 
	# $@: $?

# This naming convention comes from the eric IDE.
$(gui)/Ui_%.py: $(gui)/%.ui
	# $@: $?
	pyuic4 -x "$<" > "$@"
