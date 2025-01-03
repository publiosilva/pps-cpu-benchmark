import argparse
import base64
import io
import statistics
import time

import matplotlib.pyplot as plt


def is_prime(num):
    for i in range(2, num // 2):
        if num % i == 0:
            return True
    return False


def count_primes(round_duration):
    start_time = time.time()
    num = 2
    prime_count = 0

    while time.time() - start_time < round_duration:
        if is_prime(num):
            prime_count += 1
        num += 1

    pps = prime_count / round_duration
    return pps, num


def save_csv(rounds, output_filename, pps, max_nums):
    csv = 'round,pps,max_num\n'

    for i in range(rounds):
        csv += f'{i + 1},{pps[i]},{max_nums[i]}\n'

    with open(f'{output_filename}.csv', 'w') as file:
        file.write(csv)


def create_gauge_chart(mean_pps):
    _, ax = plt.subplots(figsize=(6, 3))
    ax.barh(0, mean_pps, color='black')
    ax.set_xlim(0, 15000)
    ax.set_yticks([])
    ax.axvspan(0, 5000, color='red', alpha=0.5)
    ax.axvspan(5000, 10000, color='yellow', alpha=0.5)
    ax.axvspan(10000, 15000, color='green', alpha=0.5)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return base64.b64encode(buf.read()).decode('utf-8')


def create_line_chart(values, title, xlabel, ylabel):
    _, ax = plt.subplots()
    ax.plot(list(range(len(values))), values, marker='o', linestyle='-', color='b')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    y_max = max(values) if values else 1
    ax.set_ylim(bottom=0, top=y_max * 1.1)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return base64.b64encode(buf.read()).decode('utf-8')


def save_html(pps, max_nums, output_filename):
    mean_pps = statistics.mean(pps)
    median_pps = statistics.median(pps)
    stddev_pps = statistics.stdev(pps)
    variance_pps = statistics.variance(pps)

    mean_max = statistics.mean(max_nums)
    median_max = statistics.median(max_nums)
    stddev_max = statistics.stdev(max_nums)
    variance_max = statistics.variance(max_nums)

    gauge_chart = create_gauge_chart(mean_pps)
    line_chart_pps = create_line_chart(pps, "PPS Evolution Over Rounds", "Round", "PPS")
    line_chart_max = create_line_chart(max_nums, "Max Number Variation Over Rounds", "Round", "Max Number")

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PPS Results</title>
        <style>
            body {{ text-align: center; font-family: Arial, sans-serif; }}
            .container {{ width: 80%; margin: 0 auto; }}
            .velocimeter, .line-chart {{ margin: 50px auto; }}
            .stats-table {{ margin: 50px auto; }}
            .avg-pps {{ font-size: 32px; font-weight: bold; margin: 20px auto; }}
            table {{ width: 100%; border: 1px solid #ddd; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: center; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="avg-pps">
                Mean PPS: {mean_pps}
            </div>
            <div class="velocimeter">
                <img src="data:image/png;base64,{gauge_chart}" alt="Velocimeter Chart">
            </div>
            <div class="line-chart">
                <img src="data:image/png;base64,{line_chart_pps}" alt="PPS Line Chart">
            </div>
            <div class="line-chart">
                <img src="data:image/png;base64,{line_chart_max}" alt="Max Number Line Chart">
            </div>
            <h3>Statistics for PPS</h3>
            <div class="stats-table">
                <table border="1" style="margin: 0 auto;">
                    <tr><th>Statistic</th><th>Value</th></tr>
                    <tr><td>Mean</td><td>{mean_pps}</td></tr>
                    <tr><td>Median</td><td>{median_pps}</td></tr>
                    <tr><td>Standard Deviation</td><td>{stddev_pps}</td></tr>
                    <tr><td>Variance</td><td>{variance_pps}</td></tr>
                </table>
            </div>
            <h3>Statistics for Max Numbers</h3>
            <div class="stats-table">
                <table border="1" style="margin: 0 auto;">
                    <tr><th>Statistic</th><th>Value</th></tr>
                    <tr><td>Mean</td><td>{mean_max}</td></tr>
                    <tr><td>Median</td><td>{median_max}</td></tr>
                    <tr><td>Standard Deviation</td><td>{stddev_max}</td></tr>
                    <tr><td>Variance</td><td>{variance_max}</td></tr>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    with open(f'{output_filename}.html', 'w') as file:
        file.write(html_template)


def main(rounds, round_duration, output_filename):
    pps = []
    max_nums = []

    for _ in range(rounds):
        prime_count, max_num = count_primes(round_duration)
        pps.append(prime_count)
        max_nums.append(max_num)

    save_csv(rounds, output_filename, pps, max_nums)
    save_html(pps, max_nums, output_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PPS CPU Benchmark')

    parser.add_argument('--rounds', '-r', type=int, default=6, help='Number of rounds')
    parser.add_argument('--duration', '-d', type=int, default=10, help='Duration of each round in seconds')
    parser.add_argument('--output', '-o', default='./pps-result', help='Output file name')

    args = parser.parse_args()

    main(rounds=args.rounds, round_duration=args.duration, output_filename=args.output)
