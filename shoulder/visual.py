import numpy as np
from matplotlib import pyplot as plt

from .enums import MuscleCoefficientPlots, MuscleSurfacePlots
from .models import ModelAbstract


class Plotter:

    def __init__(
        self,
        model: ModelAbstract,
        t: np.ndarray = None,
        q: np.ndarray = None,
        qdot: np.ndarray = None,
        tau: np.ndarray = None,
        emg: np.ndarray = None,
        muscle_index: int | range | slice | None = None,
        dof_index: int | range | slice | None = None,
    ):

        # Store the data
        self._model = model
        self._t = t
        self._q = q
        self._qdot = qdot
        self._tau = tau
        self._emg = emg
        self._muscle_index = muscle_index
        self._dof_index = dof_index

    def plot_muscle_surface(self, plots: list[MuscleSurfacePlots], axis_id: int):
        if isinstance(plots, MuscleSurfacePlots):
            plots = [plots]

        for plot in plots:
            if plot == MuscleSurfacePlots.NONE:
                continue
            elif plot == MuscleSurfacePlots.COEFFICIENTS:
                self.plot_muscle_force_coefficients_surface(axis_id)
            elif plot == MuscleSurfacePlots.FORCE:
                self.plot_muscle_force_surface(axis_id)
            else:
                raise NotImplementedError(f"Plot {plot} not implemented")

    def plot_muscle_force_coefficients_surface(self, axis_id: int):
        if self._q is None or self._qdot is None or self._emg is None:
            raise ValueError("q, qdot and emg must be provided to plot the muscle force coefficients surface")

        # Draw the surface of the force-length-velocity relationship for each model
        fig = plt.figure("Force-Length-Velocity relationship (coefficients)")
        length, velocity = self._model.muscles_kinematics(self._q, self._qdot)

        x, y = np.meshgrid(self._q[self._dof_index, :], self._qdot[self._dof_index, :])
        z = np.ndarray((velocity.shape[1], length.shape[1]))

        for i in range(length.shape[1]):
            q_rep = np.repeat(self._q[:, i : i + 1], self._qdot.shape[1], axis=1)
            _, flce, fvce = self._model.muscle_force_coefficients(self._emg, q_rep, self._qdot, self._muscle_index)
            z[:, i] = flce * fvce

        ax = fig.add_subplot(axis_id, projection="3d")
        ax.plot_surface(x, y, z, cmap="viridis")
        ax.set_xlabel("q")
        ax.set_ylabel("qdot")
        ax.set_zlabel("Force (normalized)")
        ax.set_zlim(0, ax.get_zlim()[1])
        ax.set_title(self._model.name)

    def plot_muscle_force_surface(self, axis_id: int):
        if self._q is None or self._qdot is None or self._emg is None:
            raise ValueError("q, qdot and emg must be provided to plot the muscle force surface")

        # Draw the surface of the force-length-velocity relationship for each model
        fig = plt.figure("Force-Length-Velocity relationship (maximal force)")
        length, velocity = self._model.muscles_kinematics(self._q, self._qdot)

        x, y = np.meshgrid(self._q[self._dof_index, :], self._qdot[self._dof_index, :])
        z = np.ndarray((velocity.shape[1], length.shape[1]))

        for i in range(length.shape[1]):
            q_rep = np.repeat(self._q[:, i : i + 1], self._qdot.shape[1], axis=1)
            z[:, i] = self._model.muscle_force(self._emg, q_rep, self._qdot, self._muscle_index)

        ax = fig.add_subplot(axis_id, projection="3d")
        ax.plot_surface(x, y, z, cmap="viridis")
        ax.set_xlabel("q")
        ax.set_ylabel("qdot")
        ax.set_zlabel("Force (N)")
        ax.set_zlim(0, ax.get_zlim()[1])
        ax.set_title(self._model.name)

    def plot_movement(self):
        if self._t is None:
            raise ValueError("t must be provided to plot the movement")

        plt.figure()
        n_subplots = sum(x is not None for x in [self._q, self._qdot, self._tau, self._emg])
        subplot_index = 1

        if self._q is not None:
            plt.subplot(n_subplots, 1, subplot_index)
            plt.plot(self._t, self._q.T)
            plt.title("Position")
            plt.xlabel("Time")
            plt.ylabel("Q")
            subplot_index += 1

        if self._qdot is not None:
            plt.subplot(n_subplots, 1, subplot_index)
            plt.plot(self._t, self._qdot.T)
            plt.title("Velocity")
            plt.xlabel("Time")
            plt.ylabel("Qdot")
            subplot_index += 1

        if self._tau is not None:
            plt.subplot(n_subplots, 1, subplot_index)
            plt.step(self._t[[0, -1]], self._tau[np.newaxis, :][[0, 0], :])
            plt.title("Torque")
            plt.xlabel("Time")
            plt.ylabel("Tau")
            subplot_index += 1

        if self._emg is not None:
            plt.subplot(n_subplots, 1, subplot_index)
            plt.step(self._t[[0, -1]], self._emg[np.newaxis, :][[0, 0], :])
            plt.title("EMG")
            plt.xlabel("Time")
            plt.ylabel("EMG")

    @staticmethod
    def show():
        plt.show()

    def plot_muscle_force_coefficients(
        self,
        plots: list[MuscleCoefficientPlots],
        color: str,
        plot_right_axis: bool = True,
        fig: dict[str, list] = None,
    ) -> dict[str, list]:
        if isinstance(plots, MuscleCoefficientPlots):
            plots = [plots]
        if len(plots) == 0 or (len(plots) == 1 and plots[0] == MuscleCoefficientPlots.NONE):
            return None

        flpe, flce, fvce = self._model.muscle_force_coefficients(
            self._emg, self._q, self._qdot, muscle_index=self._muscle_index
        )
        y_left = []
        y_left.append(flpe)
        y_left.append(flce)
        y_left.append(fvce)

        length, velocity = self._model.muscles_kinematics(self._q, self._qdot, self._muscle_index)
        y_right = []
        y_right.append(length)
        y_right.append(length)
        y_right.append(velocity)

        if fig is None:
            fig = {}
        y_right_label = []
        y_right_label.append("Muscle length")
        y_right_label.append("Muscle length")
        y_right_label.append("Muscle velocity")
        y_right_color = "g"
        for x_axis in plots:
            title = []
            x = []
            x_label = []
            if x_axis == MuscleCoefficientPlots.NONE:
                continue
            if x_axis == MuscleCoefficientPlots.TIME:
                title.append("Passive Force-Length relationship (Time)")
                title.append("Active Force-Length relationship (Time)")
                title.append("Active Force-Velocity relationship (Time)")

                x.append(self._t)
                x_label.append("Time (s)")

                x.append(self._t)
                x_label.append("Time (s)")

                x.append(self._t)
                x_label.append("Time (s)")

            elif x_axis == MuscleCoefficientPlots.MUSCLE_PARAMETERS:
                title.append("Passive Force-Length relationship (Muscle parameters)")
                title.append("Active Force-Length relationship (Muscle parameters)")
                title.append("Active Force-Velocity relationship (Muscle parameters)")

                x.append(length[0, :])
                x_label.append("Muscle length")

                x.append(length[0, :])
                x_label.append("Muscle length")

                x.append(velocity[0, :])
                x_label.append("Muscle velocity")

            elif x_axis == MuscleCoefficientPlots.KINEMATICS:
                title.append("Passive Force-Length relationship (Kinematics)")
                title.append("Active Force-Length relationship (Kinematics)")
                title.append("Active Force-Velocity relationship (Kinematics)")

                x.append(self._q[self._dof_index, :])
                x_label.append("q")

                x.append(self._q[self._dof_index, :])
                x_label.append("q")

                x.append(self._qdot[self._dof_index, :])
                x_label.append("qdot")

            else:
                raise NotImplementedError(f"X axis {x_axis} not implemented")

            for j in range(len(y_left)):
                if title[j] in fig:
                    plt.figure(fig[title[j]][0])
                else:
                    fig[title[j]] = [plt.figure(title[j])]

                if len(fig[title[j]]) < 2:
                    fig[title[j]].append(plt.gca())
                else:
                    plt.axes(fig[title[j]][1])  # index 0 is fig

                for i in range(len(x[j])):
                    n_points = x[j].shape[0]
                    label = self._model.name if i == len(x[j]) - 1 else None
                    plt.plot(x[j][i], y_left[j][:, i], f"{color}o", alpha=i / n_points, label=label)

                plt.legend(loc="upper left")
                plt.xlabel(x_label[j])
                plt.ylabel("Force (normalized)")

            for j in range(len(y_right)):
                if plot_right_axis:
                    # On the right axis, plot the muscle length
                    fig_tp = fig[title[j]]
                    plt.figure(fig_tp[0])
                    if len(fig_tp) < 3:
                        fig_tp.append(plt.twinx())
                    else:
                        plt.axes(fig_tp[2])  # index 0 is fig

                    for i in range(len(x[j])):
                        n_points = x[j].shape[0]
                        label = y_right_label[j] if i == len(x[j]) - 1 else None
                        plt.plot(x[j][i], y_right[j][:, i], f"{y_right_color}o", alpha=i / n_points, label=label)

                    plt.legend(loc="upper right")
                    plt.ylabel(y_right_label[j])
        return fig
