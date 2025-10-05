import base64

text = "hello"
print("Original text:", text)

text_bytes = text.encode('utf-8')
print("As bytes:", text_bytes)

encoded_bytes = base64.b64encode(text_bytes)
print("Base64 bytes:", encoded_bytes)

encoded_text = encoded_bytes.decode('utf-8')
print("Base64 string:", encoded_text)

decoded_bytes = base64.b64decode(encoded_text)
decoded_text = decoded_bytes.decode('utf-8')
print("Decoded back:", decoded_text)