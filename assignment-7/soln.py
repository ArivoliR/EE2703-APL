import numpy as np
from matplotlib import pyplot as plt


def dist(src: tuple, pt: tuple, mic: float) -> float:
    d1 = np.sqrt(np.square(src[1] - pt[1]) + np.square(src[0] - pt[0]))
    d2 = np.sqrt(np.square(mic - pt[1]) + np.square(pt[0]))
    return d1 + d2


def wsrc(t: float, SincP: float) -> float:
    return np.sinc(SincP * t)


def generate_microphone_positions(Nmics: int, pitch: float) -> list:
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
    t_data = []
    for mic_y in mics:
        total_distance = dist((0, 0), reflector_pos, mic_y)
        t_points = [(i * dist_per_sam - total_distance) for i in range(num_samples)]
        t_data.append(wsrc(np.array(t_points) / C, SincP))
    return np.array(t_data)


def image_reconstruction(t_data, pitch, dist_per_sam, num_samples):
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
    Nmics = 64
    Nsamp = 200
    obstacle = (3, -1)
    pitch = 0.1
    dist_per_sam = 0.1
    C = 2.0
    SincP = 20

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

    #t_samples = np.loadtxt("rx3.txt")
    final_image = image_reconstruction(t_samples, pitch, dist_per_sam, Nsamp)
    plt.imshow(final_image)
    plt.savefig("reconstructed_image.png", dpi=300, bbox_inches="tight")
    plt.show()
