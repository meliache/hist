from hist import axis, NamedHist
import boost_histogram as bh
import pytest
import numpy as np
import itertools
from uncertainties import unumpy as unp


def test_basic_usage():
    """
        Test basic usage -- whether NamedHist are properly derived from\
        boost-histogram and whether it can be filled by names.
    """

    """
    Initialization
    """
    # basic
    h = NamedHist(axis.Regular(10, 0, 1, name="x")).fill(x=[0.35, 0.35, 0.45])

    for idx in range(10):
        if idx == 3:
            assert h[idx] == h[{0: idx}] == h[{"x": idx}] == 2
        elif idx == 4:
            assert h[idx] == h[{0: idx}] == h[{"x": idx}] == 1
        else:
            assert h[idx] == h[{0: idx}] == h[{"x": idx}] == 0

    # with named axes
    assert NamedHist(
        axis.Regular(50, -3, 3, name="x"), axis.Regular(50, -3, 3, name="y")
    ).fill(x=np.random.randn(10), y=np.random.randn(10))

    assert NamedHist(axis.Bool(name="x"), axis.Bool(name="y")).fill(
        y=[True, False, True], x=[True, False, True]
    )

    assert NamedHist(
        axis.Variable(range(-3, 3), name="x"), axis.Variable(range(-3, 3), name="y")
    ).fill(x=np.random.randn(10), y=np.random.randn(10))

    assert NamedHist(axis.Integer(-3, 3, name="x"), axis.Integer(-3, 3, name="y")).fill(
        x=np.random.randn(10), y=np.random.randn(10)
    )

    assert NamedHist(
        axis.IntCategory(range(-3, 3), name="x"),
        axis.IntCategory(range(-3, 3), name="y"),
    ).fill(x=np.random.randn(10), y=np.random.randn(10))

    assert NamedHist(
        axis.StrCategory(["F", "T"], name="x"), axis.StrCategory("FT", name="y")
    ).fill(y=["T", "F", "T"], x=["T", "F", "T"])

    """
    Fill
    """
    # Regular
    h = NamedHist(
        axis.Regular(10, 0, 1, name="x"),
        axis.Regular(10, 0, 1, name="y"),
        axis.Regular(2, 0, 2, name="z"),
    ).fill(
        x=[0.35, 0.35, 0.35, 0.45, 0.55, 0.55, 0.55],
        y=[0.35, 0.35, 0.45, 0.45, 0.45, 0.45, 0.45],
        z=[0, 0, 1, 1, 1, 1, 1],
    )

    z_one_only = h[{"z": bh.loc(1)}]
    for idx_x in range(0, 10):
        for idx_y in range(0, 10):
            if idx_x == 3 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 4 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 5 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 3
                )
            else:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 0
                )

    # Bool
    h = NamedHist(axis.Bool(name="x"), axis.Bool(name="y"), axis.Bool(name="z"),).fill(
        x=[True, True, True, True, True, False, True],
        y=[False, True, True, False, False, True, False],
        z=[False, False, True, True, True, True, True],
    )

    z_one_only = h[{"z": bh.loc(True)}]
    assert z_one_only[False, False] == z_one_only[{"x": False, "y": False}] == 0
    assert z_one_only[False, True] == z_one_only[{"x": False, "y": True}] == 1
    assert z_one_only[True, False] == z_one_only[{"x": True, "y": False}] == 3
    assert z_one_only[True, True] == z_one_only[{"x": True, "y": True}] == 1

    # Variable
    h = NamedHist(
        axis.Variable(range(11), name="x"),
        axis.Variable(range(11), name="y"),
        axis.Variable(range(3), name="z"),
    ).fill(
        x=[3.5, 3.5, 3.5, 4.5, 5.5, 5.5, 5.5],
        y=[3.5, 3.5, 4.5, 4.5, 4.5, 4.5, 4.5],
        z=[0, 0, 1, 1, 1, 1, 1],
    )

    z_one_only = h[{"z": bh.loc(1)}]
    for idx_x in range(0, 10):
        for idx_y in range(0, 10):
            if idx_x == 3 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 4 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 5 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 3
                )
            else:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 0
                )

    # Integer
    h = NamedHist(
        axis.Integer(0, 10, name="x"),
        axis.Integer(0, 10, name="y"),
        axis.Integer(0, 2, name="z"),
    ).fill(
        x=[3.5, 3.5, 3.5, 4.5, 5.5, 5.5, 5.5],
        y=[3.5, 3.5, 4.5, 4.5, 4.5, 4.5, 4.5],
        z=[0, 0, 1, 1, 1, 1, 1],
    )

    z_one_only = h[{"z": bh.loc(1)}]
    for idx_x in range(0, 10):
        for idx_y in range(0, 10):
            if idx_x == 3 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 4 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 5 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 3
                )
            else:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 0
                )

    # IntCategory
    h = NamedHist(
        axis.IntCategory(range(10), name="x"),
        axis.IntCategory(range(10), name="y"),
        axis.IntCategory(range(2), name="z"),
    ).fill(
        x=[3.5, 3.5, 3.5, 4.5, 5.5, 5.5, 5.5],
        y=[3.5, 3.5, 4.5, 4.5, 4.5, 4.5, 4.5],
        z=[0, 0, 1, 1, 1, 1, 1],
    )

    z_one_only = h[{"z": bh.loc(1)}]
    for idx_x in range(0, 10):
        for idx_y in range(0, 10):
            if idx_x == 3 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 4 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 1
                )
            elif idx_x == 5 and idx_y == 4:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 3
                )
            else:
                assert (
                    z_one_only[idx_x, idx_y]
                    == z_one_only[{"x": idx_x, "y": idx_y}]
                    == 0
                )

    # StrCategory
    h = NamedHist(
        axis.StrCategory("FT", name="x"),
        axis.StrCategory(list("FT"), name="y"),
        axis.StrCategory(["F", "T"], name="z"),
    ).fill(
        x=["T", "T", "T", "T", "T", "F", "T"],
        y=["F", "T", "T", "F", "F", "T", "F"],
        z=["F", "F", "T", "T", "T", "T", "T"],
    )

    z_one_only = h[{"z": bh.loc("T")}]
    assert z_one_only[bh.loc("F"), bh.loc("F")] == 0
    assert z_one_only[bh.loc("F"), bh.loc("T")] == 1
    assert z_one_only[bh.loc("T"), bh.loc("F")] == 3
    assert z_one_only[bh.loc("T"), bh.loc("T")] == 1

    """
    Projection
    """
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Bool(name="B", title="b [units]"),
        axis.Variable(range(11), name="C", title="c [units]"),
        axis.Integer(0, 10, name="D", title="d [units]"),
        axis.IntCategory(range(10), name="E", title="e [units]"),
        axis.StrCategory("FT", name="F", title="f [units]"),
    )

    # ToDo: shouldn't work -- move to test_errors when finished
    # via indices
    for num in range(6):
        for int_perm in list(itertools.permutations(range(0, 6), num)):
            assert h.project(*int_perm)

    # via names
    for num in range(6):
        for str_perm in list(
            itertools.permutations(["A", "B", "C", "D", "E", "F"], num)
        ):
            assert h.project(*str_perm)

    """
    Plot1d
    """
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
    ).fill(A=np.random.normal(size=10))

    assert h.plot1d(color="green", ls="--", lw=3)

    """
    Plot2d
    """
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
    ).fill(B=np.random.normal(size=10), A=np.random.normal(size=10))

    assert h.plot2d(cmap="cividis")

    """
    Plot2d_full
    """
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
    ).fill(B=np.random.normal(size=10), A=np.random.normal(size=10))

    assert h.plot2d_full(
        main_cmap="cividis",
        top_ls="--",
        top_color="orange",
        top_lw=2,
        side_ls="-.",
        side_lw=1,
        side_color="steelblue",
    )

    """
    Plot
    """
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
    ).fill(A=np.random.normal(size=10))

    assert h.plot(color="green", ls="--", lw=3)

    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
    ).fill(B=np.random.normal(size=10), A=np.random.normal(size=10))

    assert h.plot(cmap="cividis")

    """
    Plot Pull
    """
    h = NamedHist(
        axis.Regular(
            50, -4, 4, name="S", title="s [units]", underflow=False, overflow=False
        )
    ).fill(S=np.random.normal(size=10))

    def pdf(x, a=1 / np.sqrt(2 * np.pi), x0=0, sigma=1, offset=0):
        exp = unp.exp if a.dtype == np.dtype("O") else np.exp
        return a * exp(-((x - x0) ** 2) / (2 * sigma ** 2)) + offset

    assert h.plot_pull(
        pdf,
        eb_ecolor="crimson",
        eb_mfc="crimson",
        eb_mec="crimson",
        eb_fmt="o",
        eb_ms=6,
        eb_capsize=1,
        eb_capthick=2,
        eb_alpha=0.8,
        vp_c="gold",
        vp_ls="-",
        vp_lw=8,
        vp_alpha=0.6,
        fp_c="chocolate",
        fp_ls="-",
        fp_lw=3,
        fp_alpha=1.0,
        bar_fc="orange",
        pp_num=6,
        pp_fc="orange",
        pp_alpha=0.618,
        pp_ec=None,
    )


def test_errors():
    """
        Test errors -- whether the name exceptions in the NamedHist are thrown.
    """

    """
    Initialization
    """
    # with no-named axes
    with pytest.raises(Exception):
        NamedHist(
            axis.Regular(50, -3, 3, name=""), axis.Regular(50, -3, 3, name="")
        ).fill(x=np.random.randn(10), y=np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(axis.Bool(name=""), axis.Bool(name="")).fill(
            y=[True, False, True], x=[True, False, True]
        )

    with pytest.raises(Exception):
        NamedHist(axis.Variable(range(-3, 3)), axis.Variable(range(-3, 3))).fill(
            x=np.random.randn(10), y=np.random.randn(10)
        )

    with pytest.raises(Exception):
        NamedHist(axis.Integer(-3, 3), axis.Integer(-3, 3)).fill(
            x=np.random.randn(10), y=np.random.randn(10)
        )

    with pytest.raises(Exception):
        NamedHist(
            axis.IntCategory(range(-3, 3), name=""),
            axis.IntCategory(range(-3, 3), name=""),
        ).fill(x=np.random.randn(10), y=np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(
            axis.StrCategory(["F", "T"], name=""), axis.StrCategory("FT", name="")
        ).fill(y=["T", "F", "T"], x=["T", "F", "T"])

    # with duplicated names
    with pytest.raises(Exception):
        NamedHist(axis.Regular(50, -3, 3, name="x"), axis.Regular(50, -3, 3, name="x"))

    with pytest.raises(Exception):
        NamedHist(axis.Bool(name="y"), axis.Bool(name="y"))

    with pytest.raises(Exception):
        NamedHist(
            axis.Variable(range(-3, 3), name="x"), axis.Variable(range(-3, 3), name="x")
        )

    with pytest.raises(Exception):
        NamedHist(axis.Integer(-3, 3, name="x"), axis.Integer(-3, 3, name="x"))

    with pytest.raises(Exception):
        NamedHist(
            axis.IntCategory(range(-3, 3), name="x"),
            axis.IntCategory(range(-3, 3), name="x"),
        )

    with pytest.raises(Exception):
        NamedHist(
            axis.StrCategory("TF", name="y"), axis.StrCategory(["T", "F"], name="y")
        )

    """
    Fill
    """
    # without names
    with pytest.raises(Exception):
        NamedHist(
            axis.Regular(50, -3, 3, name="x"), axis.Regular(50, -3, 3, name="y")
        ).fill(np.random.randn(10), np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(axis.Bool(name="x"), axis.Bool(name="y")).fill(
            [True, False, True], [True, False, True]
        )

    with pytest.raises(Exception):
        NamedHist(
            axis.Variable(range(-3, 3), name="x"), axis.Variable(range(-3, 3), name="y")
        ).fill(np.random.randn(10), np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(axis.Integer(-3, 3, name="x"), axis.Integer(-3, 3, name="y")).fill(
            np.random.randn(10), np.random.randn(10)
        )

    with pytest.raises(Exception):
        NamedHist(
            axis.IntCategory(range(-3, 3), name="x"),
            axis.IntCategory(range(-3, 3), name="y"),
        ).fill(np.random.randn(10), np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(
            axis.StrCategory(["F", "T"], name="x"), axis.StrCategory("FT", name="y")
        ).fill(["T", "F", "T"], ["T", "F", "T"])

    # wrong names
    with pytest.raises(Exception):
        NamedHist(
            axis.Regular(50, -3, 3, name="x"), axis.Regular(50, -3, 3, name="y")
        ).fill(x=np.random.randn(10), z=np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(axis.Bool(name="x"), axis.Bool(name="y")).fill(
            y=[True, False, True], z=[True, False, True]
        )

    with pytest.raises(Exception):
        NamedHist(
            axis.Variable(range(-3, 3), name="x"), axis.Variable(range(-3, 3), name="y")
        ).fill(z=np.random.randn(10), x=np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(axis.Integer(-3, 3, name="x"), axis.Integer(-3, 3, name="y")).fill(
            x=np.random.randn(10), z=np.random.randn(10)
        )

    with pytest.raises(Exception):
        NamedHist(
            axis.IntCategory(range(-3, 3), name="x"),
            axis.IntCategory(range(-3, 3), name="y"),
        ).fill(y=np.random.randn(10), z=np.random.randn(10))

    with pytest.raises(Exception):
        NamedHist(
            axis.StrCategory(["F", "T"], name="x"), axis.StrCategory("FT", name="y")
        ).fill(z=["T", "F", "T"], x=["T", "F", "T"])

    def pdf(x, a=1 / np.sqrt(2 * np.pi), x0=0, sigma=1, offset=0):
        exp = unp.exp if a.dtype == np.dtype("O") else np.exp
        return a * exp(-((x - x0) ** 2) / (2 * sigma ** 2)) + offset

    h = NamedHist(
        axis.Regular(
            50, -4, 4, name="X", title="s [units]", underflow=False, overflow=False
        )
    ).fill(X=np.random.normal(size=10))

    """
    Projection
    """
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Bool(name="B", title="b [units]"),
        axis.Variable(range(11), name="C", title="c [units]"),
        axis.Integer(0, 10, name="D", title="d [units]"),
        axis.IntCategory(range(10), name="E", title="e [units]"),
        axis.StrCategory("FT", name="F", title="f [units]"),
    )

    # duplicated
    with pytest.raises(Exception):
        h.project(0, 0)

    with pytest.raises(Exception):
        h.project("A", "A")

    # wrong/mixed types
    with pytest.raises(Exception):
        h.project(2, "A")

    with pytest.raises(Exception):
        h.project(True, "A")

    # cannot found
    with pytest.raises(Exception):
        h.project(-1, 9)

    with pytest.raises(Exception):
        h.project("G", "H")

    """
    Plot1d
    """
    # dimension error
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
    ).fill(B=np.random.normal(size=10), A=np.random.normal(size=10))

    with pytest.raises(Exception):
        h.plot1d()

    # wrong kwargs names
    with pytest.raises(Exception):
        h.project("A").plot1d(abc="red")

    # wrong kwargs type
    with pytest.raises(Exception):
        h.project("B").plot1d(ls="red")

    """
    Plot2d
    """
    # dimension error
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
    ).fill(B=np.random.normal(size=10), A=np.random.normal(size=10))

    with pytest.raises(Exception):
        h.project("A").plot2d()

    # wrong kwargs names
    with pytest.raises(Exception):
        h.plot2d(abc="red")

    # wrong kwargs type
    with pytest.raises(Exception):
        h.plot2d(cmap=0.1)

    """
    Plot2d_full
    """
    # dimension error
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
    ).fill(B=np.random.normal(size=10), A=np.random.normal(size=10))

    with pytest.raises(Exception):
        h.project("A").plot2d_full()

    # wrong kwargs names
    with pytest.raises(Exception):
        h.plot2d_full(abc="red")

    with pytest.raises(Exception):
        h.plot2d_full(color="red")

    # wrong kwargs type
    with pytest.raises(Exception):
        h.plot2d_full(main_cmap=0.1, side_lw="autumn")

    """
    Plot
    """
    # dimension error
    h = NamedHist(
        axis.Regular(
            50, -5, 5, name="A", title="a [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="B", title="b [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="C", title="c [units]", underflow=False, overflow=False
        ),
    ).fill(
        A=np.random.normal(size=10),
        B=np.random.normal(size=10),
        C=np.random.normal(size=10),
    )

    with pytest.raises(Exception):
        h.plot()

    # wrong kwargs names
    with pytest.raises(Exception):
        h.project("A").plot(abc="red")

    with pytest.raises(Exception):
        h.project("A", "C").plot(abc="red")

    # wrong kwargs type
    with pytest.raises(Exception):
        h.project("B").plot(ls="red")

    with pytest.raises(Exception):
        h.project("A", "C").plot(cmap=0.1)

    """
    Plot Pull
    """
    # dimension error
    hh = NamedHist(
        axis.Regular(
            50, -4, 4, name="X", title="s [units]", underflow=False, overflow=False
        ),
        axis.Regular(
            50, -4, 4, name="Y", title="s [units]", underflow=False, overflow=False
        ),
    ).fill(X=np.random.normal(size=10), Y=np.random.normal(size=10))

    with pytest.raises(Exception):
        hh.plot_pull(pdf)

    # not callable
    with pytest.raises(Exception):
        h.plot_pull("1")

    with pytest.raises(Exception):
        h.plot_pull(1)

    with pytest.raises(Exception):
        h.plot_pull(0.1)

    with pytest.raises(Exception):
        h.plot_pull((1, 2))

    with pytest.raises(Exception):
        h.plot_pull([1, 2])

    with pytest.raises(Exception):
        h.plot_pull({"a": 1})

    # wrong kwargs names
    with pytest.raises(Exception):
        h.plot_pull(pdf, abc="crimson", xyz="crimson")

    with pytest.raises(Exception):
        h.plot_pull(pdf, ecolor="crimson", mfc="crimson")

    # disabled params
    with pytest.raises(Exception):
        h.plot_pull(pdf, eb_label="value")

    with pytest.raises(Exception):
        h.plot_pull(pdf, vp_label="value")

    with pytest.raises(Exception):
        h.plot_pull(pdf, fp_label="value")

    with pytest.raises(Exception):
        h.plot_pull(pdf, ub_label="value")

    with pytest.raises(Exception):
        h.plot_pull(pdf, bar_label="value")

    with pytest.raises(Exception):
        h.plot_pull(pdf, pp_label="value")

    with pytest.raises(Exception):
        h.plot_pull(pdf, ub_color="green")

    with pytest.raises(Exception):
        h.plot_pull(pdf, bar_width=1.0)

    # wrong kwargs types
    with pytest.raises(Exception):
        h.plot_pull(pdf, eb_ecolor=1.0, eb_mfc=1.0)  # kwargs should be str