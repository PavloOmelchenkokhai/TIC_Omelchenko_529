import os
import math
import numpy as np
from scipy import fftpack
from PIL import Image
from huffman import HuffmanTree

# DCT
def dct_2d(image):
    return fftpack.dct(fftpack.dct(image.T, norm='ortho').T, norm='ortho')


def idct_2d(image):
    return fftpack.idct(fftpack.idct(image.T, norm='ortho').T, norm='ortho')


# КВАНТУВАННЯ
def load_quantization_table(component):
    return np.array([
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ])

if not os.path.exists("Results"):
    os.makedirs("Results")

def quantize(block, component, q_scale=1):
    Q = load_quantization_table(component) * q_scale
    return np.round(block / Q)


def dequantize(block, component, q_scale=1):
    Q = load_quantization_table(component) * q_scale
    return block * Q


# ZIGZAG
def zigzag_points(rows, cols):
    points = []
    for s in range(rows + cols - 1):
        if s % 2 == 0:
            for i in range(s + 1):
                j = s - i
                if i < rows and j < cols:
                    points.append((i, j))
        else:
            for i in range(s + 1):
                j = s - i
                if j < rows and i < cols:
                    points.append((j, i))
    return points


def block_to_zigzag(block):
    return [int(block[i][j]) for i, j in zigzag_points(8, 8)]


def zigzag_to_block(zigzag):
    block = np.zeros((8, 8))
    for index, (i, j) in enumerate(zigzag_points(8, 8)):
        block[i][j] = zigzag[index]
    return block


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def run_length_encode(arr):
    result = []
    count = 1

    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            count += 1
        else:
            result.append((arr[i - 1], count))
            count = 1

    result.append((arr[-1], count))
    return result


def write_to_file(filepath, bitstream):
    with open(filepath, "w") as f:
        f.write(bitstream)


# ENCODE
def encode():
    if not os.path.exists("Results"):
        os.makedirs("Results")

    results_summary = []

    for filename in os.listdir("."):
        if not filename.endswith(".bmp"):
            continue

        for q_scale in [1, 2]:

            print(f"Processing: {filename}, Q={q_scale}")

            image = Image.open(filename).convert('L')
            image = np.array(image)
            h, w = image.shape

            reconstructed = np.zeros_like(image)
            all_symbols = []

            for i in range(0, h, 8):
                for j in range(0, w, 8):
                    block = image[i:i+8, j:j+8]

                    if block.shape != (8, 8):
                        continue

                    dct_block = dct_2d(block)
                    q_block = quantize(dct_block, "lum", q_scale)

                    zz = block_to_zigzag(q_block)
                    rle = run_length_encode(zz)

                    for val, count in rle:
                        all_symbols.append((val, count))

                    deq = dequantize(q_block, "lum", q_scale)
                    idct_block = idct_2d(deq)

                    reconstructed[i:i+8, j:j+8] = idct_block

            tree = HuffmanTree(all_symbols)
            code_table = tree.value_to_bitstring_table()

            if '' in code_table.values():
                for k in code_table:
                    code_table[k] = '0'

            encoded_data = ''.join(code_table[s] for s in all_symbols)

            txt_name = f"Results/{filename[:-4]}_Q{q_scale}.txt"
            with open(txt_name, "w") as f:
                f.write(encoded_data)

            reconstructed = np.clip(reconstructed, 0, 255)
            img_out = Image.fromarray(reconstructed.astype(np.uint8))

            img_name = f"Results/{filename[:-4]}_Q{q_scale}.jpg"
            img_out.save(img_name)

            original_size = os.path.getsize(filename) * 8
            compressed_size = len(encoded_data)

            cr = round(original_size / compressed_size, 2) if compressed_size != 0 else 0

            results_summary.append(
                f"{filename} Q={q_scale} | CR={cr} | size={compressed_size} bits"
            )

    with open("results_jpeg.txt", "w") as f:
        for line in results_summary:
            f.write(line + "\n")

    print("Все виконано")


class JPEGFileReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        with open(self.filepath, "r") as f:
            return f.read()


# DECODE
def decoder():
    for filename in os.listdir("."):
        if filename.endswith("_encoded.txt"):
            print(f"Decoding: {filename}")

            reader = JPEGFileReader(filename)
            bitstream = reader.read()

            print(f"Size: {len(bitstream)} bits")


if __name__ == "__main__":
    encode()
    decoder()