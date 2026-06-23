import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you doing today? I hope you're having a great day!"

token = enc.encode(text)

print(token,"Number of tokens:", len(token))

dec = [13225, 11, 1495, 553, 481, 5306, 4044, 30, 357, 5498, 7163, 4566, 261, 2212, 2163, 0]
decoder = enc.decode(dec)

print(decoder, "Number of characters:", len(decoder))

