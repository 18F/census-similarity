# Census Similarity

A small set of commands for finding similarity between data sets

## Installation with Docker

The simplest installation is to use the automatically-built Docker image.
Docker can be thought of like a very-fast virtual machine that carries around
all of its environment dependencies with it. It communicates with the outside
world through stdin and stdout.

To install/run using Docker, you'll need to have Docker installed and then
preface each command (see [Usage](#usage)) with

```
docker run -it --rm 18fgsa/census-similarity
```

That tells docker to accept input from stdin and delete the app after
execution. As it's a bit of a mouthful, we recommend using a shorthand
variable:

```
census="docker run -it --rm 18fgsa/census-similarity"

# e.g.
cat some.csv | census group_by
```

## Installation via Python

We'll assume you've already
[cloned](https://help.github.com/articles/cloning-a-repository/)
[this repository](https://github.com/18F/census-similarity.git),
[installed Python3](https://wiki.python.org/moin/BeginnersGuide/Download), 
and set up a
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Next, try
```
pip install -r requirements.txt
```

If this fails, look at the error message for a missing C library. You may also
try the instructions provided by [SciPy](https://www.scipy.org/install.html).

## Usage

This application consists of several small utilities which should be strung
together to get a useful result. We provide some examples below, but we can't
list all of the relevant permutations. Not only can the utilities be combined
but several have additional parameters that users may want to tune to their
dataset.

### Commands

Execute a command and add the `--help` for a more thorough description, but at
the high level:

* `cluster_by_field` finds similar rows in a CSV based on a single field. This
  has multiple tuning parameters
* `group_by` groups rows of a CSV by values in a particular column
* `lookup` replaces "id"s with their names based on a lookup file

### Examples

For these examples, we'll assume two files:

* `dataset.csv` - metadata about datasets, with columns `id` and `name`
* `vars.csv` - metadata about fields within those datasets. It contains
  columns `vname` (name of field), `dsids` (a column containing a
  comma-separated list of dataset ids)

We'll be trying to find similar datasets.

#### Clustering by dataset name
First, let's take a very simple approach: we'll cluster the datasets by
looking at similar dataset names:

```
cat dataset.csv | cluster_by_field | group_by --min-group-size 2
```

Let's break that down:
* `cat dataset.csv` - print the CSV to stdout
* `cluster_by_field` - cluster those CSVs using default settings. This command
  appends a new column to the CSV which includes the cluster id. Default
  values for parameters are:
    * `eps` is  0.10 (the maximum distance to consider when clustering)
    * `min-samples` is 2 (the number of samples needed to form a cluster)
    * `distance-metric` is "jaccard" (many ways to find the distance between
      strings)
    * `field` is "name" (what field to look at when clustering)
    * `field-split` is "character" (how to treat the entries within that
      field). Character means we are looking at a sequence of characters as
      opposed to a sequence of trigrams or a comma-separated list
    * `group-field` is "_group" (column name to store the cluster ids)
* `group_by` - groups CSV rows by values in a particular field. The output
  will have one row for every distinct value in the "group-field" column.
  We're using the default settings save `min-group-size`, notably:
    * `group-field` is "_group" (what field we want to group by)
    * `accumulation-field` is "id" (the column we want to collect)
    * `min-group-size` is 2 (defaults to 1) -- this is the minimum size group
      we want to include in the results

The output of the above will include one row for each dataset cluster, listing
the ids within that cluster. While very useful, that's not a very nice visual.
If we wanted to collect dataset names instead, we'd run:

```
cat dataset.csv \
  | cluster_by_field \
  | group_by --min-group-size 2 --accumulation-field name
```

A second method of achieving the same result would be to "lookup" the dataset
names by referencing their ids:

```
cat dataset.csv \
  | cluster_by_field \
  | group_by --min-group-size 2 \
  | lookup --lookup-file dataset.csv --replacement-field id
```

* `lookup` converts ids from one CSV into their respective values, using a
  second CSV as the lookup source. Two fields must always be specified, while
  the other two have reasonable defaults.
  * `lookup-file` the file name we'll be using to find id-value pairs.
    "dataset.csv" in the above example
  * `replacement-field` the CSV column that contains ids we want to replace.
    We expect those ids to be comma-separated
  * `id-field` the CSV column that contains the ids in the lookup-file.
    Defaults to "id"
  * `value-field` the CSV column that contains the value in the lookup-file.
    Defaults to "name"


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
