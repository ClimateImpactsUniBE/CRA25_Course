
# Guide to set up Conda Environments for Python

> Author: Daniel Steinfeld, modified to personal PC's (02.2025)

Conda is an open source *package* and *environment* management system that lets you quickly and easily install, run and update programming languages like Python, R and many more. In this guide, we will focus on Python.

Conda helps you to set up Python programming environments, in which you can develop and run applications. An environment is a directory, that contains the Python version and the packages that are completely compatible with your application. It is best practice to set up environments for each project. Why?

- Because you may need other versions of Python/packages for different applications and you want to make sure that older applications are still working.
- You are sharing your code or collaborating with someone else and you want to make sure that it is working on their computer ("reproducibility in science").

The following steps will help you with setting up conda environments on your personal computer.

## Step 1: Install miniconda

There are (at least) three different conda installers:

- Miniconda
- Anaconda
- Miniforge

All come with **Conda** (package & environment management system) and with a **root or base environment**. Main difference are: Miniconda requires only 400MB disk space and contains only a few basic packages. Anaconda requires 3GB disk space and installs automatically over 250+ packages and also a GUI (graphical user interface) called Anaconda Navigator. Miniforge is like Miniconda but comes with **mamba**, a faster version of conda, and has the conda-forge channel enabled and highest priority by default. It is the preferred choice. Do make sure you only have one of those installed at a time.

1. Download the latest installer for your operating system from here (Regular installation):  
- Miniconda or Anaconda: <https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation>
- Miniforge: <https://github.com/conda-forge/miniforge/releases/tag/24.11.3-0>

If you have a Mac, download the "arm64" version if you have a m1, m2 or m3 processor, otherwise "x86_64". On Linux, most probably "x86_64".

2. In your terminal, run:

    **For Linux and macOS**
    ```bash
    # this is a comment
    $ bash Miniforge3-$(uname)-$(uname -m).sh
    ```
    **For Windows**: double-click .exe file

3. Follow the instructions on the screen by accepting the defaults with "yes".
4. Test your installation.  

    On Linux and maCOS:  
    close and then re-open your terminal window.  
    On Windows:  
    Start menu, open the miniforge Prompt.

    ```bash
    # A list of installed packages
    $ conda list 
    
    # Information about conda version
    $ conda info
    conda x.xx.x # Output
    ```

By default, conda is installed in your *home* directory:  
Linux: `/home/steidani/miniforge3/`  
Windowd: `C:\Users\steidani\miniforge3\`  
In case conda or python is not recognized in your terminal/prompt, you'll have to initialize it after the installation process. 
On Mac/Linux, first run `source <path to miniforge>/bin/activate` and then run `conda init`.
On Windows, first run `<path to miniforge>\bin\activate` and then run `conda init`.

If you have installed miniforge, you can choose to use **mamba** instead of **conda** in the rest of this tutorial. It is essentially the same thing but faster, and is used in exactly the same way with exactly the same syntax. I will stick with **conda** in the tutorial.

## Extra: Uninstalling conda
To uninstall conda, just remove the folder (Carefully, this will also delete all your environments, see Step 2):

```bash
# undo the modifications made by conda init, if you ran this command
$ conda init --reverse --all
# remove miniforge3 folder 
$ rm -rf ~/miniforge3
```
## Extra: Updating conda
To update conda to the current version (you should do this from time to time), in terminal window or Anaconda Prompt, run

```bash
# update conda
$ conda update conda
```

### Extra: Adding channel priority
This is already done for you if you installed miniforge.

Conda has many different channels, from which packages are downloaded. This can sometimes cause channel collisions. Read more [here](https://conda.io/projects/conda/en/latest/user-guide/concepts/channels.html).

You can modify what channels are automatically searched for packages. [conda-forge](https://conda-forge.org/docs/index.html) is a channel that hosts and maintains almost all packages.

To install packages from conda-forge, add it as the highest priority channel:

```bash
# Add conda-forge as the highest priority channel
$ conda config --add channels conda-forge
```

Conda is now installed, and we can create our first environment and install packages.

## Step 2: Create an environment and install Python packages

Detailed information on how to manage environments can be found here:  
<https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>

It is best practice to keep your 'base' clean and install packages into environments.

1. Create a new (empty) environment with the name myenv

    ```bash
    # create environment 'mynev'
    $ conda create --name myenv

    # list all your environments
    $ conda env list
    ```

    Environments are stored here: `/home/steidani/miniconda3/envs`

2. Activate environment

    ```bash
    # activate environment 'myenv'
    $ conda activate myenv
    ```

    The active environment, the one you are currently using, is shown in parentheses () at the beginning of your prompt:  
    `(myenv) $`

    Check which Python version is installed.

    ```bash
    # This is a comment: Check the python version
    (myenv) $ python3 -V
    Python 3.8.10 
    ```

3. Install Python packages in the active environment with  
   `conda install <package_name>`  
   For example numpy:

    ```bash
    (myenv) $ conda install numpy
    # Note: all dependencies of numpy are also installed. Accept with 'yes'.

    # list all installed packages in myenv
    (myenv) $ conda list
    ```

4. Deactivate environment (going back to 'base')

    ```bash
    (myenv) $ conda deactivate
    $ # or (base) $
    ```

**Warning**  
Use `pip` as little as possible. Favor `conda` or `mamba` with the `conda-forge` channel.

### Extra

You can also create an environment from an existing `environment.yml` text file. This is a nice way to share your environment with colleagues. We are giving you such a file with all the packages required to run the notebooks and that also should be sufficient for your project.

```bash
# create environment based on environment.yml
$ conda env create -f environment.yml
```

An `environment.yml` (with some packages to analyze weather and climate data) looks like this:

    name: cra_env
    channels:
    - conda-forge
    dependencies:
    - python=3.12
    - xarray
    - dask
    - ipython
    - intake
    - intake-esm
    - aiohttp
    - fsspec
    - cartopy
    - matplotlib
    - jupyterlab
    - scipy
    - netcdf4
    - s3fs
    - ca-certificates
    - certifi
    - openssl
    - seaborn

    prefix: /PATH/TO/miniforge3/envs/cra_env

To create an `environment.yml` based on your environment, run

```bash
(cra_env) $ conda env export --from-history > environment.yml
```

Don't forget to update `environment.yml` after installing additional packages.

We are giving you a premade environment with all you shoud need. It was created on February 13 using the following command:
```bash
# create environment for CRA
$ mamba create --name cra_env python=3.12 xarray netCDF4 dask IPython jupyterlab intake intake-esm aiohttp fsspec matplotlib cartopy scipy s3fs seaborn
```

## Step 3: Decide on an IDE

An IDE (Integrated development environment) is a comprehensive text editor to write, test, debug and run your code in an easier way. Popular Python IDEs are:

- [VScode](https://code.visualstudio.com/)
- [Jupyter notebooks](https://jupyter.org/)
- [Pycharm](https://www.jetbrains.com/de-de/pycharm/)
- [Spyder](https://www.spyder-ide.org/)
- and many more ...

Which Python IDE is right for you? Only you can decide that :)  
Spyder has a similar interface to Rstudio and Matlab. Jupyter notebooks are very popular in science for sharing documents that integrate live code, computational output, visualizations and text. Personally, I use Visual Studio Code which needs some configuration (installing extensions) at the beginning, but now I also use it for documentation (markdown, LaTex). It can run python files, IPython code cells and Jupyter notebooks when the correct extensions are installed.

In any case, I recommend installing jupyter directly into your environment and use it to share codes and results:  
`(cra_env) $ conda install -c conda-forge jupyterlab`

## Step 4: Test if it works

In the folder *Tutorial0_python_install* you'll find a Jupyter notebook called **test_notebook.ipynb**. Try to run it to see if your installation works! No worries if not, we'll help you in the first tutorial lesson if necessary.

## Step 5: What's next?

Now that you've set up your python programming environment, I recommend you play around with it. Best is to work trough some online tutorials and get familiar with different python packages, the IDE and conda.

Here are some great tutorials:

- Python:
  - for beginner (basic python): <https://docs.python.org/3/tutorial/>
  - Getting started with Python for Science, including packages numpy, scipy and matplotlib: <http://scipy-lectures.org/intro/index.html>
  - for more advanced Python user, I'll recommend the summer school at UZH: <https://www.physik.uzh.ch/~python/python_2021-06/index.php.html>
    - all lecture notes are online and can be found under 'Programme'  

- packages you should know (each with their own guide on how to install and get started):
  - [numpy](https://numpy.org/): creating and manipulating numerical data and multi-dimensional arrays
  - [scipy](https://www.scipy.org/): scientific computing
  - [pandas](https://pandas.pydata.org/): working with tabular data and time series (similar to R dataframe)
  - [matplotlib](https://matplotlib.org/): for plotting
  - [cartopy](https://scitools.org.uk/cartopy/docs/latest/): for plotting on a map
  - [xarray](http://xarray.pydata.org/en/stable/): reading and manipulating netcdf data (build on top of numpy and pandas, very popular in the climate science community)
  - [scikit-learn](https://scikit-learn.org/stable/): statistical learning
  - [metpy](https://unidata.github.io/MetPy/latest/index.html): collection of functions for calculations with weather data
  - and many more :)
    - you can even create your own packages and share them with others, example: <https://github.com/steidani/ConTrack>

- [git](https://git-scm.com/) for version control:

    “Version control is a system that records changes to a file or set of
    files over time so that you can recall specific versions later.”  
    <https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control>

  - beginners git course of C2SM: <https://github.com/C2SM/git-course>
