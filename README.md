# Chaotic System Simulator

This is a Python program that allows you to simulate and visualize various chaotic systems using a graphical user interface (GUI). The program uses the `tkinter` library for the GUI, `matplotlib` for plotting, and other libraries for sound generation and playback.

## Installation

To run this program, you need to have Python installed on your system. You can download Python from the official website: [python.org](https://python.org).

In addition, the program requires the following dependencies:

- `matplotlib`
- `numpy`
- `pydub`

You can install these dependencies using `pip` by running the following command:
```cmd
pip install matplotlib numpy pydub
```

## Usage

To run the program, execute the following command:
```cmd
python Khaos.py
```

Upon running the program, a GUI window titled "Chaotic System Simulator" will open. The GUI provides various options and sliders to control and visualize different chaotic systems.

### System Selection

The topmost dropdown menu allows you to select the system you want to simulate. The available options are:

- Logistic Map: Simulates the logistic map and displays the resulting bifurcation diagram.
- Lorenz System: Simulates the Lorenz system and displays the resulting trajectory in 3D.
- Bifurcation Diagram: Displays the bifurcation diagram for a given range of parameters.

### Parameter Sliders

The parameters for each system are controlled using sliders. The sliders are dynamically generated based on the selected system. The available sliders for each system are as follows:

- Logistic Map: Sliders for r (growth rate) and x0 (initial value).
- Lorenz System: Sliders for sigma, rho, beta (system parameters), x0, y0, z0 (initial values), and dt (time step).
- Bifurcation Diagram: Sliders for r (growth rate), x0 (initial value), num_iterations (number of iterations), and skip (number of iterations to skip before plotting).

### Plotting

The program displays the results of the selected system in a plot area. The plot is automatically updated whenever you change the system or adjust the parameter sliders. The type of plot depends on the selected system:

- Logistic Map: Shows the bifurcation diagram with x values plotted against r.
- Lorenz System: Shows the trajectory of the Lorenz system in 3D space.
- Bifurcation Diagram: Shows the bifurcation diagram with x values plotted against r.

### Sound Generation

The program also provides a "Play Sound" button. However, the sound generation feature is currently implemented only for the **Logistic Map** system. Clicking the button will generate a sound based on the logistic map simulation. The pitch of the sound is determined by the `x` values of the logistic map, ranging from 440Hz (A4) to 1320Hz (E6).

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue on the GitHub repository: [https://github.com/Khosraw/Khaos/](https://github.com/Khosraw/Khaos/)

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this code as permitted by the license.
