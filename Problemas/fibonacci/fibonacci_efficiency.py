
"""
Fibonacci efficiency comparison: recursive vs iterative vs fast-doubling
Saves CSVs and PNGs in the current directory.
"""
from dataclasses import dataclass
from typing import Tuple, List
import time, math, csv
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class FibResult:
    n: int
    value: int
    steps: int
    time_ms: float
    algo: str

def fib_recursive_with_counts(n: int) -> Tuple[int, int]:
    if n < 2:
        return n, 1
    v1, s1 = fib_recursive_with_counts(n-1)
    v2, s2 = fib_recursive_with_counts(n-2)
    return v1 + v2, s1 + s2 + 1

def fib_iterative_with_counts(n: int) -> Tuple[int, int]:
    if n < 2:
        return n, 1
    a, b = 0, 1
    steps = 1
    for _ in range(2, n+1):
        a, b = b, a + b
        steps += 1
    return b, steps

def fib_fast_doubling_with_counts(n: int) -> Tuple[int, int]:
    def fd(k: int):
        if k == 0:
            return 0, 1, 1
        f_k, f_k1, s = fd(k >> 1)
        c = f_k * ((f_k1 << 1) - f_k)
        d = f_k*f_k + f_k1*f_k1
        if k & 1:
            return d, c + d, s + 1
        else:
            return c, d, s + 1
    f_n, _, steps = fd(n)
    return f_n, steps

def run_and_time(fn, n_list, name: str):
    out = []
    for n in n_list:
        t0 = time.perf_counter()
        val, steps = fn(n)
        dt = (time.perf_counter() - t0)*1000.0
        out.append(FibResult(n, val, steps, dt, name))
    return out

def main():
    n_small = [0,1,2,3,5,8,10,15,20,25,30,35]
    res_small = []
    res_small += run_and_time(fib_recursive_with_counts, [x for x in n_small if x <= 35], "recursive")
    res_small += run_and_time(fib_iterative_with_counts, n_small, "iterative")
    res_small += run_and_time(fib_fast_doubling_with_counts, n_small, "fast_doubling")
    df_small = pd.DataFrame([r.__dict__ for r in res_small])
    df_small.to_csv("fib_small.csv", index=False)

    plt.figure()
    for algo in df_small['algo'].unique():
        sub = df_small[df_small['algo'] == algo]
        plt.plot(sub['n'].values, sub['time_ms'].values, marker='o', label=algo)
    plt.yscale('log')
    plt.xlabel('n'); plt.ylabel('tempo (ms) [log]'); plt.title('Tempo vs n (até 35)'); plt.legend()
    plt.savefig("fib_small_time.png", dpi=160, bbox_inches="tight")

    plt.figure()
    for algo in df_small['algo'].unique():
        sub = df_small[df_small['algo'] == algo]
        plt.plot(sub['n'].values, sub['steps'].values, marker='o', label=algo)
    plt.yscale('log')
    plt.xlabel('n'); plt.ylabel('passos [log]'); plt.title('Passos vs n (até 35)'); plt.legend()
    plt.savefig("fib_small_steps.png", dpi=160, bbox_inches="tight")

    n_large = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    res_large = []
    res_large += run_and_time(fib_iterative_with_counts, n_large, "iterative")
    res_large += run_and_time(fib_fast_doubling_with_counts, n_large, "fast_doubling")
    df_large = pd.DataFrame([r.__dict__ for r in res_large])
    df_large['digits'] = df_large['value'].apply(lambda x: 1 if x == 0 else int(math.log10(x)) + 1)
    df_large.drop(columns=['value']).to_csv("fib_large.csv", index=False)

    plt.figure()
    for algo in df_large['algo'].unique():
        sub = df_large[df_large['algo'] == algo]
        plt.plot(sub['n'].values, sub['time_ms'].values, marker='o', label=algo)
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel('n [log]'); plt.ylabel('tempo (ms) [log]'); plt.title('Tempo (n grandes)'); plt.legend()
    plt.savefig("fib_large_time.png", dpi=160, bbox_inches="tight")

    plt.figure()
    for algo in df_large['algo'].unique():
        sub = df_large[df_large['algo'] == algo]
        plt.plot(sub['n'].values, sub['steps'].values, marker='o', label=algo)
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel('n [log]'); plt.ylabel('passos [log]'); plt.title('Passos (n grandes)'); plt.legend()
    plt.savefig("fib_large_steps.png", dpi=160, bbox_inches="tight")

if __name__ == "__main__":
    import pandas as pd
    main()
