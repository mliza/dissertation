import re

def figure_settings():
    fig_config = { }
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6 #3.5
    fig_config["fig_height"] = 5 #2.5
    fig_config["dpi_size"] = 600
    fig_config["axis_label_size"] = 14
    fig_config["legend_size"] = 12
    fig_config["ticks_size"] = 13
    fig_config["title_size"] = 18
    return fig_config

def rename_label(key_in: str) -> str:
    allowed_keys = ["N2", "O2", "O", "N", "NO", "N2+", "O2+", "O+", "N+", "NO+"]

    if key_in not in allowed_keys:
        raise ValueError(f"Unsupported key: {key_in}")

    # Regex breakdown:
    # - ([A-Z]+): Match one or more capital letters (e.g., "N", "O", "NO")
    # - (\d?): Optionally match a single digit (e.g., "2")
    # - (\+?): Optionally match a plus sign
    match = re.fullmatch(r"([A-Z]+)(\d?)(\+?)", key_in)

    if not match:
        raise ValueError(f"Key could not be parsed: {key_in}")

    species, subscript, superscript = match.groups()

    label = f"${species}"
    if subscript:
        label += f"_{{{subscript}}}"
    if superscript:
        label += f"^{{{superscript}}}"
    label += "$"
    
    return label
