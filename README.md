# Signal Analysis Tool

An interactive Python application for generating, loading, processing, statistically analysing and visualising stochastic time-series data.

The tool was developed as a computational data-analysis project to explore the relationship between individual signal realisations, ensemble averages and time averages, while providing an interactive interface for analysing both generated and externally loaded datasets.

## Features

* Generate stochastic signal realisations using:

  * Wiener processes
  * Non-ergodic stochastic processes
* Load external datasets from CSV or TXT files
* Organise multiple signal realisations using NumPy arrays
* Calculate ensemble and time averages
* Analyse the probability distribution of signal values
* Visualise multiple realisations and statistical quantities
* Interactively control the number of samples and realisations
* Toggle individual visualisations on and off
* Export figures as PNG and EPS files
* Validate user inputs and handle data-loading errors

## Technologies

* **Python**
* **NumPy** — numerical computation and array-based data processing
* **Matplotlib** — data visualisation
* **Tkinter** — graphical user interface

## How It Works

The application supports two main workflows.

### 1. Generated Data

The user can generate multiple realisations of either a Wiener process or a non-ergodic stochastic process. The realisations are stored as NumPy arrays and used to calculate statistical quantities.

For each dataset, the tool calculates:

* Individual signal realisations
* Ensemble average
* Time average of the first realisation
* Probability density of signal values

These quantities are displayed through three visualisations.

### 2. Uploaded Data

The application can also load externally generated datasets from CSV or TXT files.

The expected structure is:

```text
Time, Signal 1, Signal 2, Signal 3, ...
0.00,  0.12,     0.21,     0.17
0.01,  0.15,     0.18,     0.19
0.02,  0.10,     0.24,     0.16
...
```

The first column represents the time vector, while each additional column represents an individual signal realisation.

## Installation

Clone the repository:

```bash
git clone https://github.com/DaveZurSan/GUI_DATA.git
cd GUI_DATA
```

Install the required dependencies:

```bash
pip install numpy matplotlib
```

Tkinter is included with most standard Python installations. On some Linux distributions, it may need to be installed separately.

## Running the Application

Run the main Python file:

```bash
python signal_analysis.py
```

The graphical interface allows you to:

1. Select the number of samples.
2. Select the number of signal realisations.
3. Select how many realisations to visualise.
4. Choose the signal type.
5. Load external datasets.
6. Update the analysis.
7. Toggle individual plots.
8. Export the generated figures.

## Project Structure

```text
GUI_DATA/
├── signal_analysis.py
├── README.md
└── requirements.txt
```

### requirements.txt

```text
numpy
matplotlib
```

## Visualisations

### Signal Realisations

Displays multiple individual realisations of the generated or uploaded stochastic process.

### Ensemble Average vs Time Average

Compares the ensemble average across realisations with the time average of the first realisation.

### Probability Density

Displays the empirical probability density of the signal values across the available realisations.

## Purpose

The project demonstrates the use of Python for:

* Data loading and organisation
* Numerical data processing
* Statistical analysis
* Data aggregation
* Data visualisation
* Interactive data exploration
* File-based data handling

It provides a compact example of a complete workflow from raw numerical data to processed statistical information and visual outputs.

