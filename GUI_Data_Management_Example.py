# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:41:50 2026

@author: David
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------------------------------------------------------------
# Signal generation
# ---------------------------------------------------------------------

def wiener_process(t, dt):
    """Generate one realisation of a Wiener process."""
    dW = np.random.normal(0.0, np.sqrt(dt), len(t) - 1)
    return np.concatenate(([0.0], np.cumsum(dW)))


def non_ergodic_process(t, amplitude=1.0, frequency=5.0, noise_std=0.5):
    """Generate one noisy sinusoidal realisation."""
    return (
        amplitude * np.sin(2 * np.pi * frequency * t)
        + np.random.normal(0.0, noise_std, len(t))
    )


# ---------------------------------------------------------------------
# Data generation and loading
# ---------------------------------------------------------------------

def generate_realizations(t, signal_type, num_realizations):
    """Generate multiple signal realisations."""
    dt = t[1] - t[0]

    if signal_type == "Ergodic":
        realizations = np.array(
            [wiener_process(t, dt) for _ in range(num_realizations)]
        )

        # Centre each realisation around zero
        realizations -= np.mean(realizations, axis=1, keepdims=True)

    elif signal_type == "Non-Ergodic":
        realizations = np.array(
            [
                non_ergodic_process(t)
                for _ in range(num_realizations)
            ]
        )

    else:
        raise ValueError("Unknown signal type.")

    return realizations


def load_data_from_file():
    """Load time-series data from a CSV or TXT file."""
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("CSV files", "*.csv"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]
    )

    if not file_path:
        return None

    try:
        data = np.loadtxt(file_path, delimiter=",")
    except ValueError:
        try:
            data = np.loadtxt(file_path)
        except Exception as exc:
            messagebox.showerror(
                "Data loading error",
                f"Could not read the selected file:\n{exc}",
            )
            return None
    except Exception as exc:
        messagebox.showerror(
            "Data loading error",
            f"Could not read the selected file:\n{exc}",
        )
        return None

    if data.ndim != 2 or data.shape[1] < 2:
        messagebox.showerror(
            "Invalid data",
            "The file must contain at least two columns: time and signal data.",
        )
        return None

    return data


# ---------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------

class SignalAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Analysis")
        self.root.geometry("1000x750")

        self.uploaded_data = None
        self.t = np.linspace(0.0, 1.0, 1000)
        self.realizations = generate_realizations(
            self.t,
            "Ergodic",
            100,
        )

        self._create_controls()
        self._create_plots()
        self.update_plot()

    # -----------------------------------------------------------------
    # GUI creation
    # -----------------------------------------------------------------

    def _create_controls(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Number of samples
        ttk.Label(
            control_frame,
            text="Num Samples:",
        ).grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.num_samples_var = tk.StringVar(value="1000")
        ttk.Entry(
            control_frame,
            textvariable=self.num_samples_var,
            width=10,
        ).grid(row=0, column=1, padx=5, pady=5)

        # Number of realisations
        ttk.Label(
            control_frame,
            text="Num Realisations:",
        ).grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

        self.num_realizations_var = tk.StringVar(value="100")
        ttk.Entry(
            control_frame,
            textvariable=self.num_realizations_var,
            width=10,
        ).grid(row=0, column=3, padx=5, pady=5)

        # Number of realisations to plot
        ttk.Label(
            control_frame,
            text="Num to Plot:",
        ).grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)

        self.num_to_plot_var = tk.StringVar(value="10")
        ttk.Entry(
            control_frame,
            textvariable=self.num_to_plot_var,
            width=10,
        ).grid(row=0, column=5, padx=5, pady=5)

        # Signal type
        ttk.Label(
            control_frame,
            text="Signal Type:",
        ).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.signal_type_var = tk.StringVar(value="Ergodic")

        self.signal_type_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.signal_type_var,
            values=("Ergodic", "Non-Ergodic", "Uploaded Data"),
            state="readonly",
            width=15,
        )
        self.signal_type_combobox.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
        )

        # Buttons
        ttk.Button(
            control_frame,
            text="Update Plot",
            command=self.update_plot,
        ).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(
            control_frame,
            text="Load Data",
            command=self.load_data,
        ).grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(
            control_frame,
            text="Save Figures",
            command=self.save_figures,
        ).grid(row=1, column=4, padx=5, pady=5)

        # Plot visibility
        self.show_realizations_var = tk.BooleanVar(value=True)
        self.show_averages_var = tk.BooleanVar(value=True)
        self.show_pdf_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            control_frame,
            text="Show Realisations",
            variable=self.show_realizations_var,
            command=self.toggle_plots,
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Checkbutton(
            control_frame,
            text="Show Averages",
            variable=self.show_averages_var,
            command=self.toggle_plots,
        ).grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        ttk.Checkbutton(
            control_frame,
            text="Show PDF",
            variable=self.show_pdf_var,
            command=self.toggle_plots,
        ).grid(row=2, column=4, columnspan=2, padx=5, pady=5)

    def _create_plots(self):
        plot_frame = ttk.Frame(self.root, padding=10)
        plot_frame.pack(
            side=tk.BOTTOM,
            fill=tk.BOTH,
            expand=True,
        )

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(
            3,
            1,
            figsize=(9, 8),
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=plot_frame,
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True,
        )

    # -----------------------------------------------------------------
    # Data processing
    # -----------------------------------------------------------------

    def update_plot(self):
        try:
            num_samples = int(self.num_samples_var.get())
            num_realizations = int(
                self.num_realizations_var.get()
            )
            num_to_plot = int(self.num_to_plot_var.get())

            if num_samples < 2:
                raise ValueError(
                    "Number of samples must be at least 2."
                )

            if num_realizations < 1:
                raise ValueError(
                    "Number of realisations must be at least 1."
                )

            if num_to_plot < 1:
                raise ValueError(
                    "Number of realisations to plot must be at least 1."
                )

        except ValueError as exc:
            messagebox.showerror(
                "Invalid input",
                str(exc),
            )
            return

        signal_type = self.signal_type_var.get()

        # Generate or load data
        if signal_type == "Uploaded Data":
            if self.uploaded_data is None:
                messagebox.showwarning(
                    "No data",
                    "Please load a CSV or TXT file first.",
                )
                return

            self.t = self.uploaded_data[:, 0]
            self.realizations = self.uploaded_data[:, 1:].T

            num_realizations = self.realizations.shape[0]

        else:
            self.t = np.linspace(
                0.0,
                1.0,
                num_samples,
            )

            self.realizations = generate_realizations(
                self.t,
                signal_type,
                num_realizations,
            )

        # Statistical calculations
        ensemble_average = np.mean(
            self.realizations,
            axis=0,
        )

        # Time average of the first realisation
        time_average = np.mean(
            self.realizations[0]
        )

        # -----------------------------------------------------------------
        # Plot 1: Realisations
        # -----------------------------------------------------------------

        self.ax1.clear()

        num_to_plot = min(
            num_to_plot,
            self.realizations.shape[0],
        )

        for i in range(num_to_plot):
            self.ax1.plot(
                self.t,
                self.realizations[i],
                alpha=0.7,
            )

        self.ax1.set_title("Signal Realisations")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Signal")
        self.ax1.grid(True, alpha=0.3)

        # -----------------------------------------------------------------
        # Plot 2: Ensemble average vs time average
        # -----------------------------------------------------------------

        self.ax2.clear()

        self.ax2.plot(
            self.t,
            ensemble_average,
            label="Ensemble Average",
        )

        self.ax2.axhline(
            time_average,
            linestyle="--",
            label="Time Average (1 realisation)",
        )

        self.ax2.set_title(
            "Ensemble Average vs Time Average"
        )
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Signal")
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)

        # -----------------------------------------------------------------
        # Plot 3: Probability density histogram
        # -----------------------------------------------------------------

        self.ax3.clear()

        self.ax3.hist(
            self.realizations.flatten(),
            bins=50,
            density=True,
            alpha=0.7,
        )

        self.ax3.set_title(
            "Probability Density of Signal Values"
        )
        self.ax3.set_xlabel("Signal")
        self.ax3.set_ylabel("Density")
        self.ax3.grid(True, alpha=0.3)

        self.fig.tight_layout()

        self.toggle_plots()

    # -----------------------------------------------------------------
    # Plot visibility
    # -----------------------------------------------------------------

    def toggle_plots(self):
        self.ax1.set_visible(
            self.show_realizations_var.get()
        )

        self.ax2.set_visible(
            self.show_averages_var.get()
        )

        self.ax3.set_visible(
            self.show_pdf_var.get()
        )

        self.fig.tight_layout()
        self.canvas.draw()

    # -----------------------------------------------------------------
    # File handling
    # -----------------------------------------------------------------

    def load_data(self):
        data = load_data_from_file()

        if data is not None:
            self.uploaded_data = data
            self.signal_type_var.set("Uploaded Data")
            self.update_plot()

    def save_figures(self):
        try:
            self.fig.tight_layout()

            self.fig.savefig(
                "signal_analysis.png",
                dpi=300,
                bbox_inches="tight",
            )

            self.fig.savefig(
                "signal_analysis.eps",
                format="eps",
                bbox_inches="tight",
            )

            messagebox.showinfo(
                "Figures saved",
                "Figures successfully saved as PNG and EPS.",
            )

        except Exception as exc:
            messagebox.showerror(
                "Save error",
                f"Could not save the figures:\n{exc}",
            )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()

    app = SignalAnalysisApp(root)

    root.mainloop()