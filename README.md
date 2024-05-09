[![DOI](https://zenodo.org/badge/634943265.svg)](https://zenodo.org/doi/10.5281/zenodo.11166874)

ESIIL Data Library
================

Welcome to the Environmental Data Science Innovation and Inclusion Lab
(ESIIL) Data Library! As an NSF-funded national synthesis center, ESIIL
is devoted to nurturing collaboration between biological and computer
sciences, propelling innovation and inclusivity across both disciplines.
Our data library showcases a diverse assortment of datasets, with each
dataset presented on its own dedicated web page for easy navigation. To
help you begin, we supply accessible R and Python code snippets for
downloading and working with each dataset. For more advanced users, we
also provide extensive tutorials and vignettes tailored to individual
datasets. Explore our vast collection and tap into the potential of
environmental data for your research today!

Click on this link to go to our data library website:
https://cu-esiil.github.io/data-library/

# Contributing 
If you have a module you would like to add, fork this repo, create a new branch with your desired changes, and then submit a pull request. The main components of a successful pull request are the following:

## Module folder
A folder containing your module's markdown and accompanying files should be named after module. Within the project, it should be placed in docs/<module_subject>.
For example, the contents of the "Downloading Sentinel-2 with AWS module" are placed in docs/remote_sensing/sentinel2_aws. Feel free to create a new subject folder if the existing folders are not appropriate.


## Markdown file
Each module folder requires a markdown file which includes the module content and code blocks. Look at an existing file within the docs folder to see the formatting style. Make sure to be thorough in each code blocks explanation. Add any relevant links to the write up. Make sure any data files that are needed to run the code are included in the module folder and a link to download them is included in the markdown. Test that the code runs and produces the expected output. Include the package versions used at the time of testing.

## Navigation
You must add your module to the nav tree in the mkdocs.yml file so that it is shown on the site. Find the top level section that pertains to your modules subject (i.e. "EDS in indian country", "Solving water"). If you are creating a new subject, create a new top level entry in the nav tree. Next, add an entry to the nav tree under the top level section for your new module. The key value will be the name that will show up on the site. The value is the path from the project repo to your module's markdown file. 

## Sitemap 
In order for Google to index your new page, it must be included in the docs/sitemap.xml file. Copy and paste one of the existing link entries, and then change the URL to the URL that your new module will have.

## Index
If you are creating a new subject for your module, add the subject and its description to the 
docs/index.md file. 
