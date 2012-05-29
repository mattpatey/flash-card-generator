

from setuptools import setup, find_packages


version = "0.1.a.dev"

install_requires = [
    "reportlab>=2.5",
    ]


setup(author="Matt Patey",
      author_email="matt.patey@gmail.com",
      description="A flashcard generator",
      include_package_data=True,
      install_requires=install_requires,
      license=open('LICENSE', 'r').read(),
      long_description=open("README.md", "r").read(),
      name="Flashcard generator",
      packages=find_packages(exclude=['ez_setup', 'tests']),
      version=version,
      zip_safe=False,
      package_data={
          'flashcardgenerator': ['de-en.txt',]
          },
      )
