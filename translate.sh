pybabel extract -F babel.cfg -k lazy_gettext -k pgettext -k ngettext -k npgettext --no-wrap -o dataviva/translations/messages.pot dataviva
pybabel update -i dataviva/translations/messages.pot -d dataviva/translations
pybabel compile -f -d dataviva/translations
