gui := squall/gui
icondir := squall/icons
widgets := $(wildcard $(gui)/*.ui)
icons := $(wildcard $(icondir)/*.qrc)

all: interfaces resources

interfaces: $(widgets:$(gui)/%.ui=$(gui)/Ui_%.py)
	# $@: $?

# This naming convention comes from the eric IDE.
$(gui)/Ui_%.py: $(gui)/%.ui
	# $@: $?
	pyuic4 -x "$<" > "$@"

resources: $(icons:$(icondir)/%.qrc=$(gui)/%_rc.py)
	# $@: $?

# This naming convention comes from pyuic4.
$(gui)/%_rc.py: $(icondir)/%.qrc
	# $@: $?
	pyrcc4 "$<" > "$@"

clean:
	rm -rfv Squall.egg-info dist $(gui)/Ui_*.py $(gui)/*_rc.py $(gui)/*.pyc squall/*.pyc
