from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='sentiment_analysis',
      version="0.0.1",
      description="Data-Saenz: Sentiment Analysis about the 2023 Argentinian Elections, what are the people saying?",
      keywords="sentiment-analysis elections data-saenz argentina politics reddit nlp ai machine-learning data-science data-analysis",
      license="MIT",
      author=["Valentin Fernandez Radovich", "Juan Cruz Guillen"],
      author_email="kullback.leibler.labs@gmail.com",
      url="https://github.com/juancruzgui/data-saenz",
      install_requires=requirements,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
