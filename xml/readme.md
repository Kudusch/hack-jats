# Convert the standard json representation to JATS xml

TODO

- [ ] References

```python
python3 convert_jats.py rubbish.json rubbish.xml
```

The JATS xml file can then be convert to other formats using pandoc

e.g. docx or pdf

```bash
pandoc rubbish.xml -f jats -o rubbish.docx
pandoc rubbish.xml -f jats --pdf-engine=xelatex -o rubbish.pdf
```
