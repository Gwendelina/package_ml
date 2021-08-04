install_requirements:
    @pip install -r requirements.txt
test:
    @run -m unittest tests/*.py
