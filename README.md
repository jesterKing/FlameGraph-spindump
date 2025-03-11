This project visualizes stack traces in hang and spin reports created through
the Activity Monitor on MacOS.

The visualization is done through Rhinoceros 3D:

* One thread, one layer
* One box per sample. Each box has user string with key "frame" and the actual
  frame information as the value
* coloring of the graph based on either set gradient, or randomized gradient per
  thread (`--use-random-colors`)

This script requires the latest version of `rhino3dm` and a recent Python 3
installation. During the development 8.17.0b1 of `rhino3dm` was used with
Python 3.11.7.

This project is forked from https://github.com/vsapsai/FlameGraph-spindump which
in turn is **heavily** inspired by remarkable
[brendangregg/FlameGraph](https://github.com/brendangregg/FlameGraph).

The code has been modernized to work with Python 3.

## Usage

The simplest form is:

`python flamegraph.py spindump.txt`

This generates a file called `flamegraph.3dm` in the current work directory. The
width of the graph is 5000 model units by default. To specify a file to write to
use `--output`:

`python flamegraph.py spindump.txt --output investigate.3dm`

If you want a different sized graph use `--width` with an integer expressing the
width in model units:

`python flamegraph.py spindump.txt --output investigate.3dm --width 2500`

Likewise the default sample height of 16 units can be changed using
`--sample-height`

`python flamegraph.py spindump.txt --output investigate.3dm --sample-height 20`
