import os
import matplotlib.pyplot as plt

TARGET_SLUDGE = 85
MAX_SLUDGE = 100


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def plot_flocculant_dose(df, output_dir):
    ensure_dir(output_dir)

    plt.figure()
    plt.plot(df["TIMESTAMP"], df["RECOMMENDED_FLOCCULANT_DOSE_L_H"])
    plt.xlabel("Date")
    plt.ylabel("Flocculant dose (L/h)")
    plt.title("Flocculant dose – last 30 days")
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = os.path.join(output_dir, "flocculant_dose.png")
    plt.savefig(path)
    plt.close()

    return path


def plot_sludge_height(df, output_dir):
    ensure_dir(output_dir)

    plt.figure()
    plt.plot(df["TIMESTAMP"], df["SLUDGE"], label="Sludge height")
    plt.axhline(TARGET_SLUDGE, linestyle="--", label="Target (85 cm)")
    plt.axhline(MAX_SLUDGE, linestyle="--", label="Limit (100 cm)")

    plt.xlabel("Date")
    plt.ylabel("Sludge height (cm)")
    plt.title("Sludge height – last 30 days")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = os.path.join(output_dir, "sludge_height.png")
    plt.savefig(path)
    plt.close()

    return path


def plot_cod_vs_dose(df, output_dir):
    ensure_dir(output_dir)

    plt.figure()
    plt.scatter(df["COD"], df["RECOMMENDED_FLOCCULANT_DOSE_L_H"])
    plt.xlabel("COD (ppm)")
    plt.ylabel("Flocculant dose (L/h)")
    plt.title("COD vs Flocculant dose")
    plt.tight_layout()

    path = os.path.join(output_dir, "cod_vs_dose.png")
    plt.savefig(path)
    plt.close()

    return path
