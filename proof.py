import base64
import sys
import zlib
from random import Random

SHAPES = [(10, -4, 20, -2, 1), (12, -4, 20, -2, 1), (18, -4, 24, -2, 1), (8, -4, 14, 2, 1), (10, -4, 10, 2, 2), (2, -2, 2, 4, 1), (4, -2, 4, 4, 2), (12, 2, 14, 4, 1), (16, 2, 20, 4, 1), (20, 2, 20, 4, 1)]

PAYLOAD = (
    'eNqNlsGy3LYVRL/IccWK9TRDggRBEARBEMTg4VGQ7CiVVJZZOFVJfiG/nQNyJHvnVHHPvt3n9oWUS+47ce9F0/VGDbex'
    '7+eu051eBJ8chRykkqNv1aiVlm4wfZBmTKOZkzJrmpw47r4rwssweJWn0KU+TEknccjUJZmGIvNwdEdb+vJSGjm4n+sf'
    'BX8UdyVuY9fPorVCTp2ahJ75o+2k8i1/7eRkGjWEnr8bRGkUCK1iZ/rUPlUIVGirQmdNmN1wyNCWW5BZhSGpMB4qtkVE'
    'mfpvavp8KsrjoUtTeqnWL1VRcyqyQgziUmQWgSJTFWmFotOHp6IGRVpNQajlVCZR1KFoQJFGkbBdMFalHlUT/tw8//W6'
    'yNDnAXUCdTKoIsKYddBZhvnQqU0qq9KjTB2yNIPcvzStuN9+9ep2KtOnsq4XqOoUepQgof6bT1IrN2iNTw0+ncqirF6h'
    'SuLVaE3qnQid60lPkp5CGZ6ECXVzwbPcJFQm1Bwfyu1oD10VHaoM5V15GQb3l1FWBU/P5qdndhFuuVI8uVGXXyc/Uk14'
    'toQBhUqbqFAmnikONUWzJ3P5FjS+KevCSKLKTVGfKnXpvcljmA4d5qyiyUO0eUp9kWkqCsrQWIZBPb70l28Sdd1tEfh2'
    'l9U3ffqmGv8nJXSHZ1INGnX4OAUYd+g1PaoIPklU9b9RNFfaUdS6MSg3H53/4KVvS4N/EJib6l8ibXwbMhuAdy9H9VAf'
    'Bt+ElsvPvRYdiJ3KTt86ZaXf8K1z65N+NcjRrGoMc1WlFm+1diN+DQa34GoiwRl/JtRoNx0GBQPezN6hZMAjU8awZBPW'
    'ZCK+RZPGaMucbNHJ5SnbMhVTrB62/zTt/S7ad/fmD/b+3XLr5/Z9vrOPemn1fP91H+UkZ/MC/aK2AWla0mz0Bx31XXvd'
    'RnntaOxIt32yh+LUPNviTNi8Jmt/wNP3eHonZQWXeMs00v3Rze5HN7lbaPG6hU9IPjo3ZskWdYGmOTeo7vmY+6jKmF5K'
    'i+cNFKgkS5/G3KUpq7rfmRnJ4PvjXqmF3RtTy6LLzOTq8d/RtO/7e6PvP6T33729iPXW5jZ8uoXHLXy8XQxbJbWcK8dy'
    'Me/kar5XPbTQduRzuTCHFScmtZHVg3XucES6H6FJkNuKG0a7aLWPWqeo9IFTn9nOF/OKQ8qM1uGQrb1h9uhxJuJMgDyP'
    'M4sN4RVnXt3N7W5wm5uCgT7llsO4R3T+7h27Yc78bd68z690jA06QRAssCPB5TVsRwz74cMDB9+ypxM1ncj2Zcf+zMmk'
    'kJZik0s+rYfNy+HyfgS2io2jv39ku25lLKIMk9z/2ajm3jdN17x37W1pxNoSUng0fmv93lzcQI329myB07Wgr+bEvbmS'
    'rQ2u9adTtl4XGBnThBs9bizw4nHCwkjtrAFGDG7srs/sQzaQr93sDdNPkO+YfIV+ssgzjWrDcqiwZhc2tkBFd21CWc7W'
    'EExu2VdX8KgoNmJkSwdmFDBioMROw+s/5tCpuRtt2yUxrN3L2tz9Pf35Ht/a/BNTmhe2wzDlB2lolZuaaZf2ahe2ZGDC'
    's/u8g5FZt7ru8gQPnqZhp61h2tmsMTDtQtNEpvRuCZbOm5iMTH1gst3H8CkYpiOX4NLKZK9MFkNganIi1xheyfgtP9KU'
    'rhxDSnk7fE75Y1mKm1T462jq+eiN6LwQW21uZXu7ifAQbq8NxLVTY20gptLPi6eu9vYGmi3qDVmNz4vnzpyuRprJx0Hp'
    'emVzMEl0XLiFRpqCTaiHzDVvkaygzqJzzfPhDnOQAJuJSiv3f/0/dKn+uZ8TCif2cbjIqs2E2o1rCFk0USWLVg/6631G'
    '8XySdTUPVKXlpGo4rBvrzWG35mxpnbHebW8Ky5hXKPPel/1sobGwndyitUAYlO15opGaqCHNpAnKuG60kiEJW2LyZcqG'
    '+z4X/CgWzmZ4W8paNju4v12kcWS61EHadev9Q8Q3EV/rrTcXWV5yt3itQdW1SxdZ51U971e9FOxQcEy6fqPK0CgnWUdg'
    'Iu9tWWkG8kgurIc7Sart8Jr3GAqJppQgC3pifpR4JrOVYNXj779HkBkl1/28GBB00sM14pahVDv4XypF5FJv/4TK+ew9'
    'xYZ/yyPo523zUGQcfUQGDsVwXzxbPEeXl9NXiGKLl7QmX0nKqISkja5nxrIvcv/379Hk3deri2IvJ1vfBhAFTfUCz7yt'
    'FrZ5q9tLixu6qoGiawfcSdWO+qur+ucuXFQJbhovgK9UQdRwEXW2NX0VeV3Ud1eufcVulAhNJuwlMeVYuyq6MrErTeL1'
    'w8TsdVmzLgKKdGZyuplXW73nTO6ZfC+PZYi/rKlVq5hT61IrtvZlbe++DRTXpzZ/bMlopa96qJL0FS8hsuLlwMTLtUO8'
    'P7Yw0Vnd9aKktwzZuZh0iJFbFrhlnlvmfqUu1R7bufLFfEwP81P6TJbRt9woU3aoWzwXiBw3OmyBvBR82p499gaBmQ47'
    'wsf8WvOkvfaUyyMd+XH4oxyhwOPxmXnXRT1+WUOdkIe5Ce20t2eudUL/aBMTXi93Q649ucrzinMtpAW2nunOdq4Tn1e8'
    'toZj4l09cOBNp5NUVocpzTPnDVozEwYmnJhwZcJH3SumfLjtcLwHoYnmrlf4mtBzeRN7Fclx4+ZCRwnkuNQc086eRebb'
    'SjyvbTwy05FgSf8DaTrX/A=='
)

def unpack_table():
    # Each row stores r, c, t0, and the number of individual pairs,
    # followed by ten triples and that many quadruples.
    data = [x-64 for x in zlib.decompress(base64.b64decode(PAYLOAD))]
    table = {}
    i = 0
    while i < len(data):
        r, c, t0, patch_count = data[i:i+4]
        i += 4
        offset_end = i + 3*len(SHAPES)
        patch_end = offset_end + 4*patch_count
        assert patch_end <= len(data) and (r,c) not in table
        offsets = [tuple(data[j:j+3]) for j in range(i, offset_end, 3)]
        patches = [tuple(data[j:j+4])
                   for j in range(offset_end, patch_end, 4)]
        table[r,c] = (t0, offsets, patches)
        i = patch_end
    return table


TABLE = unpack_table()
SEEDS = {69: 1, 97: 2, 104: 2, 109: 1, 129: 1, 133: 1, 136: 1, 140: 1, 176: 1, 197: 3}

def search(n, seed, limit):
    rng = Random(seed)
    rows = [(a, a+d, d, 2*a+d)
            for d in range(1,n+1) for a in range(1,2*n-d+1)]
    rng.shuffle(rows)
    byte_count = (len(rows)+7)//8
    raw_marks = [bytearray(byte_count) for _ in range(2*n+1)]
    raw_lengths = [bytearray(byte_count) for _ in range(n+1)]
    raw_sums = [bytearray(byte_count) for _ in range(4*n+2)]
    for i,(a,b,d,s) in enumerate(rows):
        byte,rem = divmod(i,8)
        bit = 1 << rem
        raw_marks[a][byte] |= bit
        raw_marks[b][byte] |= bit
        raw_lengths[d][byte] |= bit
        raw_sums[s][byte] |= bit
    marks = [int.from_bytes(x,'little') for x in raw_marks]
    lengths = [int.from_bytes(x,'little') for x in raw_lengths]
    sums = [int.from_bytes(x,'little') for x in raw_sums]
    del raw_marks,raw_lengths,raw_sums
    needed = lengths[1:]+marks[1:]
    answer = []
    nodes = 0

    def dfs(available, pending):
        nonlocal nodes
        nodes += 1
        if nodes > limit:
            return -1
        if not pending:
            return 1

        fewest = 2*n+1
        best = 0
        for requirement in pending:
            choices = available & needed[requirement]
            count = choices.bit_count()
            if count == 0:
                return 0
            if count < fewest:
                fewest, best = count, choices
                if count == 1:
                    break

        while best:
            bit = best & -best
            best ^= bit
            a,b,d,s = rows[bit.bit_length()-1]
            answer.append((a,b))
            pruned = marks[a] | marks[b] | lengths[d] | sums[s-1] | sums[s] | sums[s+1]
            result = dfs(available & ~pruned,
                         pending.difference((d-1,n+a-1,n+b-1)))
            if result != 0:
                return result
            answer.pop()
        return 0

    result=dfs((1<<len(rows))-1,set(range(3*n)))
    return result,answer,nodes


def blocks(t, r, c):
    _, offsets, patches = TABLE[r, c]
    for (A, p, B, q, w), (a, b, ell) in zip(SHAPES, offsets):
        yield A*t+a, B*t+b, p, q, w*t+ell
    for A, a, B, b in patches:
        yield A*t+a, B*t+b, 0, 0, 1


def construct(n):
    if n < 5 or n % 4 not in (0, 1):
        raise ValueError(n)
    t, r = divmod(n, 12)
    c = t % 3
    if t >= TABLE[r, c][0]:
        return [(x+p*j, y+q*j) for x, y, p, q, m in blocks(t, r, c)
                for j in range(m)]
    preferred = SEEDS.get(n, 0)
    for seed in [preferred] + [s for s in range(128) if s != preferred]:
        status, pairs, _ = search(n, seed, 8000)
        if status == 1:
            return pairs
        if status == 0:
            raise AssertionError(f"Exhausted all branches for n={n}")
    raise AssertionError(f"Finite search hit its budget for n={n}")


def verify(n, pairs):
    ends = sorted(x for a, b in pairs for x in (a,b))
    diffs = sorted(b-a for a,b in pairs)
    sums = sorted(a+b for a,b in pairs)
    return (ends == list(range(1, 2*n+1))
            and diffs == list(range(1, n+1))
            and all(b-a >= 2 for a,b in zip(sums,sums[1:])))


def intervals(t, r, c, kind, z):
    parts = {}
    for i, (x,y,p,q,m) in enumerate(blocks(t,r,c)):
        families = (((x,p),(y,q)), ((y-x,q-p),), ((x+y,p+q),(x+y+1,p+q)))
        for j, (start,step) in enumerate(families[kind]):
            end = start + (m-1)*step
            lo, hi = sorted((start,end))
            d = abs(step) or 1
            assert 12 % d == 0 and (m == 1 if step == 0 else m >= 12//d)
            if (z-lo) % d == 0:
                L, R = (lo-z+11)//12, (hi-z)//12
                if L <= R:
                    parts[i,j] = (L,R)
    return parts


def margins(parts, order, end, z):
    values = [parts[b][0]-parts[a][1]-1 for a,b in zip(order,order[1:])]
    if end is not None:
        values.extend((parts[order[0]][0]-(12-z)//12,
                       (end-z)//12-parts[order[-1]][1]))
    return values


def certify(r, c, t):
    assert t % 3 == c and t >= TABLE[r,c][0]
    checked = 0
    for kind, factor in enumerate((2, 1, None)):
        for z in range(12):
            at0 = intervals(t,r,c,kind,z)
            at1 = intervals(t+12,r,c,kind,z)
            assert at0.keys() == at1.keys()
            order = sorted(at0, key=at0.get)
            end0 = None if factor is None else factor*(12*t+r)
            end1 = None if factor is None else factor*(12*(t+12)+r)
            g0 = margins(at0, order, end0, z)
            g1 = margins(at1, order, end1, z)
            for a,b in zip(g0,g1):
                assert (a == b == 0 if factor is not None else 0 <= a <= b), (r,c,t,kind,z,a,b)
                checked += 1
    return checked


def main():
    assert set(TABLE) == {(r,c) for r in (0,1,4,5,8,9) for c in range(3)}
    max_threshold = 0
    periodic_cases = 0
    inequalities = 0
    for (r,c),(t0, offsets, patches) in sorted(TABLE.items()):
        assert t0 % 3 == c and len(offsets) == len(SHAPES)
        max_threshold = max(max_threshold, 12*t0+r)
        for t in range(t0,t0+12,3):
            inequalities += certify(r,c,t)
            periodic_cases += 1
    print(f"Classes: {len(TABLE)}/18, periodic cases: {periodic_cases}, "
          f"boundary checks: {inequalities}", flush=True)
    assert search(4,0,8000)[0] == 0
    finite_count = formula_count = 0
    for n in range(5,max(600,max_threshold)+1):
        if n % 4 not in (0,1):
            continue
        t,r = divmod(n,12)
        assert verify(n,construct(n)), n
        if t < TABLE[r,t%3][0]:
            finite_count += 1
        else:
            formula_count += 1
    print(f"Max threshold: {max_threshold}. Checked through {max(600,max_threshold)}: "
          f"{finite_count} finite searches, {formula_count} constructions.")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tables"]:
        print("SHAPES =", SHAPES)
        for key, value in sorted(TABLE.items()):
            print(key, value)
    else:
        main()
