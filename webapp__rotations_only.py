import streamlit as st
import plotly.graph_objects as go
import textwrap
import pandas as pd

from Qs import Q, Qs, qrandom, rotation, rotation_only, generate_QQs


def zero_out(
    q_1: Q, t: bool = False, x: bool = False, y: bool = False, z: bool = False
):
    """
    Puts a zero in one or more of the four places.
    """

    if t:
        q_1.t = 0

    if x:
        q_1.x = 0

    if y:
        q_1.y = 0

    if z:
        q_1.z = 0

    return q_1


def zero_outs(
    q_1: Qs, t: bool = False, x: bool = False, y: bool = False, z: bool = False
):
    """
    Puts a zero in one or more of the four places.
    """
    return Qs(
        [zero_out(q, t, x, y, z) for q in q_1.qs],
        qs_type=q_1.qs_type,
        rows=q_1.rows,
        columns=q_1.columns,
    )


# Sidebar setup.
Rodrigues_func = st.sidebar.checkbox(label="UqU^-1", value=True)
Rodrigues_generalized_func = st.sidebar.checkbox(
    label="UqU* + 1/2((U U q)* - (U* U* q)*)", value=False
)

# U_zero = st.sidebar.radio(label="Make one zero", options=("U.t", "U.x", "U.y", "U.z"))
the_fix = st.sidebar.radio(label="U is", options=("fixed", "random"))
zero_t = st.sidebar.checkbox(label="Zero t", value=False)
zero_x = st.sidebar.checkbox(label="Zero x", value=False)
zero_y = st.sidebar.checkbox(label="Zero y", value=False)
zero_z = st.sidebar.checkbox(label="Zero z", value=False)
dim = st.sidebar.slider(label="Dimensions", min_value=10, max_value=500, value=100)

show_code = st.sidebar.checkbox("Show code", False)

# The calculation - make a DataFrame

if the_fix == "fixed":
    Rodrigues_data = pd.DataFrame(
        zero_outs(
            generate_QQs(rotation, Q([1, 1, 2, 3]), Q([0, 3, 2, 1]), dim=dim),
            zero_t,
            zero_x,
            zero_y,
            zero_z,
        ).xyz()
    )
    Rodrigues_generalized_data = pd.DataFrame(
        zero_outs(
            generate_QQs(rotation_only, Q([1, 1, 2, 3]), Q([2, 3, 2, 1]), dim=dim),
            zero_t,
            zero_x,
            zero_y,
            zero_z,
        ).xyz()
    )

elif the_fix == "random":
    Rodrigues_data = pd.DataFrame(
        zero_outs(
            generate_QQs(rotation, Q([1, 1, 2, 3]), qrandom, dim=dim),
            zero_t,
            zero_x,
            zero_y,
            zero_z,
        ).xyz()
    )
    Rodrigues_generalized_data = pd.DataFrame(
        zero_outs(
            generate_QQs(rotation_only, Q([1, 1, 2, 3]), qrandom, dim=dim),
            zero_t,
            zero_x,
            zero_y,
            zero_z,
        ).xyz()
    )


# Main page.

st.title("Rotations Only")

fig = go.Figure()
go.Layout(margin=dict(t=500))
if Rodrigues_func:
    fig.add_trace(
        go.Scatter3d(
            {"x": Rodrigues_data[0], "y": Rodrigues_data[1], "z": Rodrigues_data[2]},
            name="rotation",
            mode="markers",
            marker=dict(size=4, opacity=0.5),
        )
    )

if Rodrigues_generalized_func:
    fig.add_trace(
        go.Scatter3d(
            {
                "x": Rodrigues_generalized_data[0],
                "y": Rodrigues_generalized_data[1],
                "z": Rodrigues_generalized_data[2],
            },
            name="Generalized rotation",
            mode="markers",
            marker=dict(size=4, opacity=0.5),
        )
    )
fig.update_layout(margin=dict(l=20, r=20, b=20, t=20))
st.write(fig)
# st.markdown("## Norm Squared Values")
#
# total = norm_squared(prod).t
# odd = norm_squared(cx_origin).t
#
# table = f"""Odd | Total
# --- | --- | ---
# {odd} | {total}"""
# st.markdown(f"{table}")


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
