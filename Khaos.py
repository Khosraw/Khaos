import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play


# Backend

def logistic_map(r, x):
    return r * x * (1 - x)

def simulate_logistic_map(r, x0, num_iterations):
    values = []
    current_value = x0
    for _ in range(num_iterations):
        current_value = logistic_map(r, current_value)
        values.append(current_value)
    return values

def lorenz_system(sigma, rho, beta, x, y, z, dt):
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    return x + dx, y + dy, z + dz

def simulate_lorenz_system(sigma, rho, beta, x0, y0, z0, dt, num_iterations):
    values = []
    current_values = np.array([x0, y0, z0])
    for _ in range(num_iterations):
        current_values = lorenz_system(sigma, rho, beta, *current_values, dt)
        values.append(current_values)
    return np.array(values)

def bifurcation_diagram(r, x0, num_iterations, skip):
    x = x0
    for i in range(num_iterations):
        if i >= skip:
            yield r, x
        x = logistic_map(r, x)

# Frontend

class ChaoticSystemSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg='black')
        self.title("Chaotic System Simulator")
        plt.style.use('dark_background')

        # Bind keys for zoom in/out
        self.bind("<plus>", self.zoom_in)
        self.bind("<minus>", self.zoom_out)
        
        self.system_var = tk.StringVar()
        self.system_var.trace("w", self.update_plot)
        system_option_menu = tk.OptionMenu(self, self.system_var, "Logistic Map", "Lorenz System", "Bifurcation Diagram")
        system_option_menu.configure(bg='gray20', fg='white')
        system_option_menu["menu"].configure(bg='gray20', fg='white')
        system_option_menu.pack()

        self.parameters_frame = tk.Frame(self, bg='black')
        self.parameters_frame.pack()

        self.sliders = {
            "Logistic Map": [
                self.create_slider("r", 0, 4, 0.01),
                self.create_slider("x0", 0, 1, 0.01)
            ],
            "Lorenz System": [
                self.create_slider("sigma", 0, 50, 0.1),
                self.create_slider("rho", 0, 50, 0.1),
                self.create_slider("beta", 0, 50, 0.1),
                self.create_slider("x0", -20, 20, 0.1),
                self.create_slider("y0", -20, 20, 0.1),
                self.create_slider("z0", -20, 20, 0.1),
                self.create_slider("dt", 0.001, 0.05, 0.001)
            ],
            "Bifurcation Diagram": [
                self.create_slider("r", 0, 4, 0.01),
                self.create_slider("x0", 0, 1, 0.01),
                self.create_slider("num_iterations", 100, 5000, 100),
                self.create_slider("skip", 50, 1000, 50)
            ]
        }
        
        sound_button = tk.Button(self, text="Play Sound", command=self.play_sound)
        sound_button.pack()

        self.fig = Figure(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.system_var.set("Logistic Map")
        
    # Function to handle zoom in
    def zoom_in(self, event):
        self.toolbar.zoom()
    
    # Function to handle zoom out
    def zoom_out(self, event):
        self.toolbar.home()

    def play_sound(self):
        system = self.system_var.get()

        if system == "Logistic Map":
            r, x0 = self.get_slider_values(system)
            results = simulate_logistic_map(r, x0, num_iterations=1000)

            sound = AudioSegment.silent(duration=1000)  # start with 1 second of silence

            for value in results:
                frequency = 440 + (value * 880)  # map x-values between 440Hz (A4) and 1320Hz (E6)
                tone_generator = Sine(frequency)
                tone = tone_generator.to_audio_segment(duration=10)  # 10ms tone for each x-value
                sound = sound.append(tone, crossfade=1)  # append tone to sound with 1ms crossfade

            play(sound)  # play the sound
        else:
            print(f"No sound implementation for {system}")


    def create_slider(self, label, from_, to, resolution):
        slider = tk.Scale(self.parameters_frame, from_=from_, to=to, resolution=resolution, label=label,
                          orient="horizontal", length=200, command=self.update_plot, bg='gray20', fg='white', troughcolor='gray10')
        slider.pack(side=tk.LEFT)
        return slider

    def get_slider_values(self, system):
        return [slider.get() for slider in self.sliders[system]]

    def update_plot(self, *args): 
        system = self.system_var.get()

        for slider in self.sliders.values():
            for s in slider:
                s.pack_forget() 

        for slider in self.sliders[system]:
            slider.pack(side=tk.LEFT)

        self.fig.clf()
        ax = self.fig.add_subplot(111, projection='3d' if system == "Lorenz System" else None)

        if system == "Logistic Map":
            r, x0 = self.get_slider_values(system)
            results = simulate_logistic_map(r, x0, num_iterations=1000)
            ax.plot(results, '.')
            ax.set_title(f"Logistic map with r={r} and x0={x0}")

        elif system == "Lorenz System":
            sigma, rho, beta, x0, y0, z0, dt = self.get_slider_values(system)
            results = simulate_lorenz_system(sigma, rho, beta, x0, y0, z0, dt, num_iterations=1000)
            ax.plot3D(results[:, 0], results[:, 1], results[:, 2])
            ax.set_title(f"Lorenz system with sigma={sigma}, rho={rho}, beta={beta}, x0={x0}, y0={y0}, z0={z0}, dt={dt}")
        
        elif system == "Bifurcation Diagram":
            r, x0, num_iterations, skip = self.get_slider_values(system)
            r_values = np.linspace(r - 1.0, r + 1.0, num_iterations)
            x_values = []
            for r in r_values:
                x_values.extend(bifurcation_diagram(r, x0, num_iterations, skip))
            r_values, x_values = zip(*x_values)
            ax.plot(r_values, x_values, ',k')
            ax.set_title(f"Bifurcation diagram with r={r}, x0={x0}, num_iterations={num_iterations}, skip={skip}")
        
        self.canvas.draw()

if __name__ == "__main__":
    app = ChaoticSystemSimulator()
    app.mainloop()
