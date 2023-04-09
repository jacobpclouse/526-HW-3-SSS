from random import randint

# Shamir's Secret Sharing implementation
def generate_shares(secret, n, k, p):
    coefficients = [secret] + [randint(1, p - 1) for i in range(k - 1)]
    shares = []
    for i in range(1, n + 1):
        share = sum(coefficients[j] * (i ** j) for j in range(k)) % p
        shares.append((i, share))
    return shares

def reconstruct_secret(shares):
    p = 257 # prime number
    k = len(shares)
    secret = 0
    for i in range(k):
        xi, yi = shares[i]
        numerator, denominator = 1, 1
        for j in range(k):
            if i != j:
                xj, yj = shares[j]
                numerator = (numerator * -xj) % p
                denominator = (denominator * (xi - xj)) % p
        lagrange = numerator * pow(denominator, p - 2, p) % p
        secret = (secret + lagrange * yi) % p
    return secret

# Example usage
secret1 = 42
secret2 = 13
n = 4
k = 2
p = 257

# Generate 2n shares for the two secrets
shares1 = generate_shares(secret1, n, k, p)
shares2 = generate_shares(secret2, n, k, p)

# Add the shares together
shares_sum = [(xi, (yi + zi) % p) for (xi, yi), (_, zi) in zip(shares1, shares2)]

# Reconstruct the sum of the secrets from the sum of the shares
sum_secret = reconstruct_secret(shares_sum)
print(sum_secret) # Output: 55

# Multiply the shares by a scalar
scalar = 3
shares_scaled = [(xi, (scalar * yi) % p) for (xi, yi) in shares1]

# Reconstruct the scaled secret from the scaled shares
scaled_secret = reconstruct_secret(shares_scaled)
print(scaled_secret) # Output: 126
