@ECHO OFF
python addons_xml_generator.py
git add *
git commit -a -m "UPDATE"
git push origin master
