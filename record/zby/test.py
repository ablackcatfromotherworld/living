import hashlib
import base64

# 要处理的原始数据
data = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmkiOiIvYnBrLXR2L1JlY29yZE5FV1MvZGVmYXVsdC9pbmRleC5tM3U4IiwibWV0aG9kIjoiR0VUIiwiZXhwIjoxNzUzMTc5OTAwfQ"

# 1. 计算 SHA-256 哈希值 (得到32字节的二进制结果)
sha256_hash = hashlib.sha256(data).digest()

# 2. 将二进制哈希值用 Base64 编码
#    注意：标准的 Base64 编码可能会在末尾补上'='，但很多实现会去掉它
base64_encoded = base64.b64encode(sha256_hash).decode('utf-8')

print(f"原始数据: {data.decode('utf-8')}")
print(f"SHA-256 + Base64 编码结果: {base64_encoded}")
print(f"结果长度: {len(base64_encoded)}")

# 输出结果:
# 原始数据: 123456
# SHA-256 + Base64 编码结果: jZae727K08KaOmKSgOaGzww/XVqL4MviY57LfgwdemM=
# 结果长度: 44  <-- 注意这里是44，因为末尾有'='填充

# 如果去掉填充符 '='
base64_unpadded = base64_encoded.rstrip('=')
print(f"\n去掉填充符后的结果: {base64_unpadded}")
print(f"去掉填充符后的长度: {len(base64_unpadded)}")

# 输出结果:
# 去掉填充符后的结果: jZae727K08KaOmKSgOaGzww/XVqL4MviY57LfgwdemM
# 去掉填充符后的长度: 43