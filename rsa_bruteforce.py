import time
import matplotlib.pyplot as plt
from Crypto.Util.number import getPrime, inverse, GCD
from rsa_encrypt import str_to_int, int_to_str

def brute_force_rsa(e, n, ciphertext, timeout):
    start_time = time.perf_counter()
    for p in range(2, n):
        if time.perf_counter() - start_time > timeout:
            return "Timed Out", None, None
        if n % p == 0:
            q = n // p
            phi = (p - 1) * (q - 1)
            try:
                d = inverse(e, phi)
                m = pow(ciphertext, d, n)
                return int_to_str(m), p, q
            except ValueError:
                continue
    return None, None, None

def generate_rsa_keypair(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537 if bits >= 16 else 17
    while GCD(e, phi) != 1:
        e += 2  
    
    d = inverse(e, phi)
    return (e, n), (d, n), p, q

def estimate_256bit_crack_time(elapsed_32bit, bits=256):
    bit_diff = bits - 32
    complexity_ratio = 2 ** (bit_diff // 2)
    estimated_time_seconds = elapsed_32bit * complexity_ratio
    return estimated_time_seconds

def format_seconds(seconds):
    if seconds < 60:
        return f"{seconds:.2e} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2e} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2e} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2e} days"
    else:
        return f"{seconds/31536000:.2e} years"

def estimate_supercomputer_time(local_seconds, local_flops=1e11, super_flops=1.1e18):
    speedup = super_flops / local_flops
    return local_seconds / speedup

# === Main Execution ===

messages = {
    2: "\x01",  # ASCII value 1
    4: "\x01",  # ASCII value 1
    8: "\x01",  # ASCII value 1
    16: "A",    # ASCII value 65
    32: "A"     # ASCII value 65
}

bit_lengths = [2, 4, 8, 16, 32]
timings = []

for bits in bit_lengths:
    print(f"\n🔐 Brute-forcing {bits}-bit RSA...")
    public, private, p, q = generate_rsa_keypair(bits)
    e, n = public
    
    message = messages[bits]
    message_int = str_to_int(message)
    
    if message_int >= n:
        print(f"⚠️ Skipping {bits}-bit: message too large for modulus n={n}")
        timings.append(0)
        continue

    ciphertext = pow(message_int, e, n)
    start = time.perf_counter()
    recovered, pf, qf = brute_force_rsa(e, n, ciphertext, timeout=1000)
    end = time.perf_counter()
    elapsed = end - start

    timings.append(elapsed)

    print(f"⏱️ Time: {elapsed:.8f}s | Recovered: {recovered} | p={pf}, q={qf}")

# === Plotting ===
plt.figure(figsize=(10, 6))
plt.semilogy(bit_lengths, timings, marker='o', linewidth=2, markersize=8)
plt.xlabel("Bit Length", fontsize=12)
plt.ylabel("Brute-force Time (s)", fontsize=12)
plt.title("Brute-force RSA Decryption Time vs Bit Length (Log Scale)", fontsize=14)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.xticks(bit_lengths)
plt.tight_layout()
plt.savefig("brute_force_times.png", dpi=300, bbox_inches='tight')
plt.show()

# === Estimations for 256-bit ===
if 32 in bit_lengths and timings[bit_lengths.index(32)] > 0:
    elapsed_32bit = timings[bit_lengths.index(32)]
    estimated_256bit_time = estimate_256bit_crack_time(elapsed_32bit)
    frontier_time = estimate_supercomputer_time(estimated_256bit_time)

    print("\n📈 Estimated Time to Crack 256-bit RSA:")
    print("🖥️  Local System:", format_seconds(estimated_256bit_time))
    print("💻  Frontier Supercomputer:", format_seconds(frontier_time))
else:
    print("\n⚠️ Could not compute 256-bit estimate: 32-bit timing missing.")
