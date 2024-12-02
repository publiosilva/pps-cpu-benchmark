# PPS CPU Benchmark

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/publiosilva/pps-cpu-benchmark.git
    cd pps-cpu-benchmark
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the benchmark with the following command:

```bash
python main.py [options]
```

### Options

| Option         | Short | Description                         | Default         |
|----------------|-------|-------------------------------------|-----------------|
| `--rounds`     | `-r`  | Number of benchmarking rounds       | `6`             |
| `--duration`   | `-d`  | Duration of each round (in seconds) | `10`            |
| `--output`     | `-o`  | Output file name                    | `./pps-result`  |

### Examples

1. Run the benchmark with default settings:
    ```bash
    python main.py
    ```

2. Run the benchmark with 8 rounds, each lasting 15 seconds, and save results to `results.csv` and `results.html`:
    ```bash
    python main.py -r 8 -d 15 -o results
    ```
