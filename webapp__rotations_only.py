import streamlit as st
import plotly.graph_objects as go
import textwrap
from PIL import Image

from Qs import (
    Q,
    qrandom,
    rotation,
    squares,
    norm_squareds,
    rotation_only,
    generate_QQs,
    zero_out,
    zero_outs,
)


# Sidebar setup.
Rodrigues_func = st.sidebar.checkbox(label="h q h⁻¹", value=True)
Rodrigues_generalized_func = st.sidebar.checkbox(label="Rotation only", value=True)
st.sidebar.markdown("Rotation only function:")
image = Image.open("images/Rodrigues_generalization.only_rotation.2_lines.png")
st.sidebar.image(image)
# U_zero = st.sidebar.radio(label="Make one zero", options=("U.t", "U.x", "U.y", "U.z"))
the_fix = st.sidebar.radio(label="U is", options=("fixed", "random"), index=1)
zero_t = st.sidebar.checkbox(label="Zero t", value=False)
zero_x = st.sidebar.checkbox(label="Zero x", value=False)
zero_y = st.sidebar.checkbox(label="Zero y", value=False)
zero_z = st.sidebar.checkbox(label="Zero z", value=False)
dim = st.sidebar.slider(label="Dimensions", min_value=10, max_value=500, value=75)

show_code = st.sidebar.checkbox("Show code", False)

# The calculation - make a DataFrame
initial_point = Q([1, 1, 2, 3])
fixed_point = Q([2, 3, 2, 1])

if the_fix == "fixed":
    Rodrigues_data = zero_outs(
        generate_QQs(rotation, initial_point, fixed_point, dim=dim),
        zero_t,
        zero_x,
        zero_y,
        zero_z,
    )
    Rodrigues_generalized_data = zero_outs(
        generate_QQs(rotation_only, initial_point, fixed_point, dim=dim),
        zero_t,
        zero_x,
        zero_y,
        zero_z,
    )

elif the_fix == "random":
    Rodrigues_data = zero_outs(
        generate_QQs(rotation, initial_point, qrandom, dim=dim),
        zero_t,
        zero_x,
        zero_y,
        zero_z,
    )
    Rodrigues_generalized_data = zero_outs(
        generate_QQs(rotation_only, initial_point, qrandom, dim=dim),
        zero_t,
        zero_x,
        zero_y,
        zero_z,
    )

# collect stats
Rodrigues_data_squares = squares(Rodrigues_data)
Rodrigues_data_norm_squares = norm_squareds(Rodrigues_data)

Rodrigues_generalized_data_squares = squares(Rodrigues_generalized_data)
Rodrigues_generalized_data_norm_squares = norm_squareds(Rodrigues_generalized_data)

# Main page.

st.title("Rotations Only")

fig = go.Figure()
go.Layout()
POINT_SIZE = 6
OPACITY = 0.5

if Rodrigues_func:
    fig.add_trace(
        go.Scatter3d(
            {
                "x": Rodrigues_data.df[1],
                "y": Rodrigues_data.df[2],
                "z": Rodrigues_data.df[3],
            },
            name="h U h⁻¹",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=OPACITY, color="violet"),
        )
    )

if Rodrigues_generalized_func:
    fig.add_trace(
        go.Scatter3d(
            {
                "x": Rodrigues_generalized_data.df[1],
                "y": Rodrigues_generalized_data.df[2],
                "z": Rodrigues_generalized_data.df[3],
            },
            name="Rotation only",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=OPACITY, color="springgreen"),
        )
    )

initial_point_zeroed = zero_out(initial_point, x=zero_x, y=zero_y, z=zero_z)
ipz_x, ipz_y, ipz_z = (
    initial_point_zeroed.x,
    initial_point_zeroed.y,
    initial_point_zeroed.z,
)
fig.add_trace(
    go.Scatter3d(
        {"x": [ipz_x], "y": [ipz_y], "z": [ipz_z]},
        name=f"Initial point: {ipz_x}, {ipz_y}, {ipz_z}",
        mode="markers",
        marker=dict(size=POINT_SIZE, opacity=OPACITY, color="red"),
    )
)

st.write(fig)

st.markdown("### Norm Squared and Squared Values")

table = f"""t² + R² | t²-R² | 2 t x | 2 t y | 2 t z
--- | --- | --- | -- | --
"""

if Rodrigues_func:
    means = Rodrigues_data_squares.df.mean()
    square = Rodrigues_data_norm_squares.df[0] / dim
    table += f"{square[0]:.2f} | {means[0]:.2f} | {means[1]:.2f} | {means[2]:.2f} | {means[3]:.2f}\n"

if Rodrigues_generalized_func:
    means = Rodrigues_generalized_data_squares.df.mean()
    square = Rodrigues_generalized_data_norm_squares.df[0] / dim
    table += f"{square[0]:.2f} | {means[0]:.2f} | {means[1]:.2f} | {means[2]:.2f} | {means[3]:.2f}"

st.markdown(f"{table}")

st.markdown(
    """### Discussion
The same quaternion, q=(1, 1, 2, 3), is the start point for all graphs. It has a quaternion norm squared of 
(15, 0, 0, 0). The squared value is (-13, 2, 4, 6). Two rotation functions can be used. The first is the Rodrigues 
rotation function developed by Olinde Rodrigues in 1843. This is applied over and over again, the number of times 
determined by the dimension value. There is also a choice for the quaternion _h_. It is either chosen randomly or can be 
fixed at a value of h=(2, 3, 2, 1).

The second function I call the Rodrigues generalized rotation function was proposed to do Lorentz boosts by D. Sweetser 
in 2010 and independently by Dr. M. Kharinov (year not known). When initially found, it was not realized that 3D
rotations were possible! A mere 3 years later, it was noticed that if the first term of the parameter _h_ was zero and 
its norm was unity, a 3D rotation would result.

The function written on one line is incorrect. Only in the Spring of 2020 have I begun to write the Rodrigues 
generalized rotation function as a two-part function like so:
"""
)
image = Image.open("images/Rodrigues_generalization_multi-part.gif")
st.image(image)
st.markdown(
    """The first part does rotations. When the parameter _h_ has a first term equal to zero, then the parameter is
normalized to one. The second part does boosts. This time the first term is used to form a hyberbolic cosine and sine
function so that its square is equal to one. The two parts of the function divide the full set of quaternions into two 
non-intersecting sets: those with a first term equal to zero and those with a non-zero first term. Each part of the 
function has three degrees of freedom, for a total of six as necessary to represent the full Lorentz group.

For this webapp, the only the first part of the Rodrigues generalized rotation function is use. This can be done by
calling the function with another function that passes a zero for the first term and the three vector terms.

The Rodrigues rotation and Rodrigues generalized rotation function are distinct. The Rodrigues rotation function uses
both real and imaginary parts of a quaternion to do a rotation. The Rodrigues generalized rotation function is 
restricted to do rotations using only the real part. The difference between the two functions can be illustrated by 
clicking the 'fixed' button. 

It would be wrong to conclude that there are some rotations that are not possible using either the Rodrigues function
or the Rodrigues generalized rotation function. The fixed calculation is a fixed value for _q_ and a fixed value for 
_h_. It can be shown analytically that for any rotation _q_ to _q'_, there is a _h_ that can be chosen to do the task.

The code used to generate the webapp and the math behind the functions can be inspected by clicking the 'show code'
button. The site can be cloned from """
)


def show_file(label: st, file_name: str, code: bool = False):
    """
    Utility to show contents of a file

    Args:
        label: str
        file_name: str
        code:

    Return: None

    """
    st.markdown("&nbsp ")
    st.markdown(f"### {label}")
    st.write(f"{file_name}")
    with open(f"{file_name}", "r") as file:
        file_lines = file.readlines()

    if code:
        st.code(textwrap.dedent("".join(file_lines[1:])))
    else:
        st.markdown(textwrap.dedent("".join(file_lines[1:])))


if show_code:
    show_file("Streamlit Webapp code", __file__, code=True)
    show_file("Qs.py library code", "Qs.py", code=True)
