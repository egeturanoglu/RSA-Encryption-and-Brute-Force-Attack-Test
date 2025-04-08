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

def estimate_supercomputer_time(local_seconds, local_flops=1e11, super_flops=1.1e18):
    speedup = super_flops / local_flops
    return local_seconds / speedup

def format_seconds(seconds):
    if seconds < 60:
        return f"{seconds:.2e} saniye"
    elif seconds < 3600:
        return f"{seconds/60:.2e} dakika"
    elif seconds < 86400:
        return f"{seconds/3600:.2e} saat"
    elif seconds < 31536000:
        return f"{seconds/86400:.2e} gün"
    else:
        return f"{seconds/31536000:.2e} yıl"

# === Ana Yürütme ===
messages = {
    2: "\x01",  # ASCII 1
    4: "\x01",
    8: "\x01",
    16: "A",
    32: "A"
}

bit_lengths = [2, 4, 8, 16, 32]
timings = []

for bits in bit_lengths:
    print(f"\n🔐 {bits}-bit RSA brute force çalıştırılıyor...")
    public, private, p, q = generate_rsa_keypair(bits)
    e, n = public
    message = messages[bits]
    message_int = str_to_int(message)
    
    if message_int >= n:
        print(f"⚠️ {bits}-bit için atlanıyor: mesaj n'den büyük, n={n}")
        timings.append(0)
        continue
    
    ciphertext = pow(message_int, e, n)
    start = time.perf_counter()
    if bits != 32:
        recovered, pf, qf = brute_force_rsa(e, n, ciphertext, timeout=1000)
    end = time.perf_counter()
    elapsed = end - start
    timings.append(elapsed)
    print(f"⏱️ Süre: {elapsed:.8f}s | Geri elde edilen mesaj: {recovered} | p={pf}, q={qf}")

# Performans karşılaştırması için grafik çizimi:
plt.figure(figsize=(10, 6))
plt.semilogy(bit_lengths, timings, marker='o', linewidth=2, markersize=8)
plt.xlabel("Bit Uzunluğu", fontsize=12)
plt.ylabel("Brute-force Süresi (s)", fontsize=12)
plt.title("Brute-force RSA Çözüm Süresi (Log Ölçek)", fontsize=14)
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.xticks(bit_lengths)
plt.tight_layout()
plt.savefig("brute_force_times.png", dpi=300, bbox_inches='tight')
plt.show()

# 32-bit RSA için ölçülen zamanı baz alarak tahmin yapalım:
index_32 = bit_lengths.index(32)
if timings[index_32] > 0:
    elapsed_32bit = timings[index_32]
    estimated_time = estimate_256bit_RSA_time(elapsed_32bit)
    frontier_time = estimate_supercomputer_time(estimated_time)
    
    print("\n📈 256-bit RSA için (modül 256-bit) tahmini kırma süresi:")
    print("🖥️  Yerel Sistem:", format_seconds(estimated_time))
    print("💻  Frontier Süper Bilgisayar:", format_seconds(frontier_time))
else:
    print("\n⚠️ 32-bit zamanlaması alınamadığı için tahmin yapılamadı.")
