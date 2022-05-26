poc:
	python3 convert_jats.py rubbish.json rubbish.xml
	pandoc rubbish.xml -f jats -o rubbish.docx
	pandoc rubbish.xml -f jats --pdf-engine=xelatex -o rubbish.pdf
