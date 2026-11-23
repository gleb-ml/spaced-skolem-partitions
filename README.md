# spaced-skolem-partitions

**Theorem.** Let $n\ge 2$ be an integer. The set $\{1,\ldots,2n\}$ can be partitioned into pairs $(a_k,b_k)$, one for each $1\le k\le n$, with $b_k-a_k=k$ and
$|(a_i+b_i)-(a_j+b_j)|\ge 2$ for every $i\ne j$, if and only if $n\ge 5$ and $n\equiv 0,1\pmod 4$.

## Files

- `proof.py` generates the pairings and checks the interval certificates.
- `tables.txt` gives the decoded block shapes, offsets, and individual pairs.
- `paper.tex` is the LaTeX source of the article.
- `paper.pdf` is the compiled article.

## Reproduce the verification

Use Python 3.10 or newer with the standard library.

```sh
python3 proof.py
python3 proof.py --tables > tables.txt
```

The verification prints these two lines.

```text
Classes: 18/18, periodic cases: 72, boundary checks: 30076
Max threshold: 233. Checked through 600: 74 finite searches, 224 constructions.
```

## Why the certificate covers every order

In each of the 18 admissible classes modulo 36, the endpoints of the intervals in the certificate are affine in $u$ after writing $t=t_*+12u$. For labels and differences, the checked gaps vanish at $u=0,1$ and hence vanish for every $u\ge 0$. For sums and their translates by one, the gaps are nonnegative at $u=0$ and have nonnegative slope. This certifies the block formulas for every order at or above its class threshold. Finite search supplies and checks a pairing for each of the 74 orders below its threshold. The direct checks through 600 also evaluate the resulting pairs.
