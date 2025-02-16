import numpy as np
from matplotlib import pyplot as plt


def dist(src: tuple, pt: tuple, mic: float) -> float:
    """
    Calculates the combined distance from a source point to a reflector point and then to a microphone.

    Args:
        src (tuple): Coordinates (x, y) of the source point.
        pt (tuple): Coordinates (x, y) of the reflector point.
        mic (float): y-coordinate of the microphone.

    Returns:
        float: Total distance from the source to the reflector and then to the microphone.
    """
    d1 = np.sqrt(np.square(src[1] - pt[1]) + np.square(src[0] - pt[0]))
    d2 = np.sqrt(np.square(mic - pt[1]) + np.square(pt[0]))
    return d1 + d2


def wsrc(t: float, SincP: float) -> float:
    """
    Generates the waveform of the source as a sinc function for the given time points.

    Args:
        t (float): Time value or array of time values.
        SincP (float): Sinc function scaling parameter.

    Returns:
        float: Sinc waveform at the given time points.
    """
    return np.sinc(SincP * t)


def generate_microphone_positions(Nmics: int, pitch: float) -> list:
    """
    Generates a list of y-coordinates for microphones arranged symmetrically around the origin.

    Args:
        Nmics (int): Number of microphones.
        pitch (float): Distance between adjacent microphones.

    Returns:
        list: Sorted list of y-coordinates for each microphone.
    """
    positions = []
    half_pitch = pitch / 2
    for i in range(Nmics // 2):
        positions.append(half_pitch + i * pitch)
        positions.append(-half_pitch - i * pitch)

    if Nmics % 2 == 1:
        positions = [pos + pitch / 2 for pos in positions]
        positions.append(-(Nmics // 2) * pitch)

    return sorted(positions)


def generate_t_samples(num_samples, mics, dist_per_sam, reflector_pos, SincP):
    """
    Generates time-domain samples for each microphone based on distances to a reflector.

    Args:
        num_samples (int): Number of samples per microphone.
        mics (list): List of y-coordinates of microphones.
        dist_per_sam (float): Distance covered per sample.
        reflector_pos (tuple): Position (x, y) of the reflector.
        SincP (float): Scaling parameter for the sinc function of the source.

    Returns:
        np.array: Array of time samples for each microphone.
    """
    t_data = []
    for mic_y in mics:
        total_distance = dist((0, 0), reflector_pos, mic_y)
        t_points = [(i * dist_per_sam - total_distance) for i in range(num_samples)]
        t_data.append(wsrc(np.array(t_points) / C, SincP))
    return np.array(t_data)


def image_reconstruction(t_data, pitch, dist_per_sam, num_samples):
    """
    Reconstructs an image by summing the time samples for each microphone over a grid of positions.

    Args:
        t_data (np.array): Array of time samples for each microphone.
        pitch (float): Distance between adjacent microphones.
        dist_per_sam (float): Distance covered per sample.
        num_samples (int): Number of samples per microphone.

    Returns:
        list: 2D list representing the reconstructed image.
    """

    mic_y_coords = [pitch * i if i != 0 else 0 for i in range(1, len(t_data) // 2 + 1)]
    mic_y_coords = sorted(
        mic_y_coords + [-pitch * i for i in range(1, len(t_data) // 2 + 1)]
    )

    max_y = (num_samples * dist_per_sam + (len(t_data) // 2) * pitch) / (2 * pitch)
    y_positions = sorted(
        [pitch * i if i != 0 else 0 for i in range(1, int(max_y))]
        + [-pitch * i for i in range(1, int(max_y))]
    )

    reconstructed_image = [
        [
            sum(
                (
                    t_data[mic_idx][
                        int(
                            dist((0, 0), (x_idx * dist_per_sam, y_pos), mic_y)
                            / dist_per_sam
                        )
                    ]
                    if int(
                        dist((0, 0), (x_idx * dist_per_sam, y_pos), mic_y)
                        / dist_per_sam
                    )
                    < len(t_data[0])
                    else 0
                )
                for mic_idx, mic_y in enumerate(mic_y_coords[: len(t_data)])
            )
            for x_idx in range(num_samples // 2)
        ]
        for y_pos in y_positions
    ]

    return reconstructed_image


if __name__ == "__main__":

    Nmics = 8  # Number of microphones
    Nsamp = 50  # Number of samples
    obstacle = (3, -1)  # Position of the obstacle
    pitch = 0.1  # Distance between microphones
    dist_per_sam = 0.1  # Distance covered per sample
    C = 0.5 # Speed of sound in the medium
    SincP = 5  # Sinc function parameter for source waveform

    mics = generate_microphone_positions(Nmics, pitch)
    t_samples = generate_t_samples(Nsamp, mics, dist_per_sam, obstacle, SincP)

    for idx, sample in enumerate(t_samples):
        plt.plot(sample + idx)
    plt.savefig("t_plot.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.clf()

    plt.imshow(t_samples)
    plt.savefig("heatmap.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.clf()

    # t_samples = np.loadtxt("rx3.txt")
    final_image = image_reconstruction(t_samples, pitch, dist_per_sam, Nsamp)
    plt.imshow(final_image)
    plt.savefig("reconstructed_image.png", dpi=300, bbox_inches="tight")
    plt.show()
